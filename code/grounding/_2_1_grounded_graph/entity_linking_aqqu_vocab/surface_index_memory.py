"""
Provides access to entities via IDs (MIDs) and surface forms (aliases).

Each entity is assigned an ID equivalent to the byte offset in the entity list
file. A hashmap stores a mapping from MID to this offset. Additionally,
another hashmap stores a mapping from surface form to this offset, along with
a score.
Matched entities with additional info (scores, other aliases) are then read
from the list file using the found offset. This avoids keeping all entities
with unneeded info in RAM.

Note: this can be improved in terms of required RAM.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>
"""
import mmap
import logging
import os
import array
import marshal

# import globals
# from common.globals_args import fn_cwq_file
# from common.hand_files import write_set
from grounding._2_1_grounded_graph.entity_linking_aqqu_vocab import entity_linker
from grounding._2_1_grounded_graph.entity_linking_aqqu_vocab.u import normalize_entity_name
import collections

logger = logging.getLogger(__name__)

class EntitySurfaceIndexMemory(object):
    """A memory based index for finding entities."""

    def __init__(self, entity_list_file, surface_map_file, entity_index_prefix):
        self.entity_list_file = entity_list_file
        self.surface_map_file = surface_map_file

        self.mid_vocabulary = self._get_entity_vocabulary(entity_index_prefix)
        self.surface_index = self._get_surface_index(entity_index_prefix)

        self.entities_mm_f = open(entity_list_file, 'r')
        self.entities_mm = mmap.mmap(self.entities_mm_f.fileno(), 0,access=mmap.ACCESS_READ)
        logger.info("Done initializing surface index.")

    def _get_entity_vocabulary(self, index_prefix):
        """Return vocabulary by building a new or reading an existing one.

        :param index_prefix:
        :return:
        """
        vocab_file = index_prefix + "_mid_vocab"
        if os.path.isfile(vocab_file):
            logger.info("Loading entity vocabulary from disk.")
            vocabulary = marshal.load(open(vocab_file, 'rb'))
        else:
            vocabulary = self._build_entity_vocabulary()
            logger.info("Writing entity vocabulary to disk.")
            marshal.dump(vocabulary, open(vocab_file, 'wb'))
        return vocabulary

    def _get_surface_index(self, index_prefix):
        """Return surface index by building new or reading existing one.

        :param index_prefix:
        :return:
        """
        surface_index_file = index_prefix + "_surface_index"
        if os.path.isfile(surface_index_file):
            logger.info("Loading surfaces from disk.")
            surface_index = marshal.load(open(surface_index_file, 'rb'))
        else:
            surface_index = self._build_surface_index()
            logger.info("Writing entity surfaces to disk.")
            marshal.dump(surface_index, open(surface_index_file, 'wb'))
        return surface_index

    def _build_surface_index(self):
        """Build the surface index.

        Reads from the surface map on disk and creates a map from
        surface_form -> offset, score ....

        :return:
        """
        n_lines = 0
        surface_index = dict()
        num_not_found = 0
        with open(self.surface_map_file, 'r',encoding="utf-8") as f:
            last_surface_form = None
            surface_form_entries = array.array('d')
            for line in f:
                n_lines += 1
                try:
                    cols = line.rstrip().split('\t')
                    surface_form = cols[0]
                    score = float(cols[1])
                    mid = cols[2]
                    entity_id = self.mid_vocabulary[mid]
                    if surface_form != last_surface_form:
                        if surface_form_entries:
                            surface_index[
                                last_surface_form] = surface_form_entries
                        last_surface_form = surface_form
                        surface_form_entries = array.array('d')
                    surface_form_entries.append(entity_id)
                    surface_form_entries.append(score)
                except KeyError:
                    num_not_found += 1
                    if num_not_found < 100:
                        logger.warn("Mid %s appears in surface map but "
                                    "not in entity list." % cols[2])
                    elif num_not_found == 100:
                        logger.warn("Suppressing further warnings about "
                                    "unfound mids.")
                if n_lines % 1000000 == 0:
                    logger.info('Stored %s surface-forms.' % n_lines)
            if surface_form_entries:
                if surface_form_entries:
                    surface_index[last_surface_form] = surface_form_entries
        logger.warn("%s entity appearances in surface map w/o mapping to "
                    "entity list" % num_not_found)
        return surface_index

    def _build_entity_vocabulary(self):
        """Create mapping from MID to offset/ID.

        :return:
        """
        logger.info("Building entity mid vocabulary.")
        mid_vocab = dict()
        num_lines = 0
        # Remember the offset for each entity.
        with open(self.entity_list_file, 'r',encoding="utf-8") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            offset = mm.tell()
            line = mm.readline()
            while line:
                num_lines += 1
                if num_lines % 1000000 == 0:
                    logger.info('Read %s lines' % num_lines)
                cols = line.decode().strip().split('\t')
                mid = cols[0]
                mid_vocab[mid] = offset
                offset = mm.tell()
                line = mm.readline()
        return mid_vocab
    '''
    @staticmethod
    def init_from_config():
        """Return an instance with options parsed by a config parser.

        :param config_options:
        :return:
        """
        config_options = globals.config
        entity_list_file = config_options.get('EntitySurfaceIndex',
                                              'entity-list')
        entity_surface_map = config_options.get('EntitySurfaceIndex',
                                                'entity-surface-map')
        entity_index_prefix = config_options.get('EntitySurfaceIndex',
                                                 'entity-index-prefix')
        return EntitySurfaceIndexMemory(entity_list_file, entity_surface_map,
                                        entity_index_prefix)
    '''
    def get_entity_for_mid(self, mid):
        """Returns the entity object for the MID or None if the MID is unknown.

        :param mid:
        :return:
        """
        try:
            offset = self.mid_vocabulary[mid]
            entity = self._read_entity_from_offset(int(offset))
            return entity
        except KeyError:
            logger.warn("Unknown entity mid: '%s'." % mid)
            return None

    def get_entities_for_surface(self, surface):
        """Return all entities for the surface form.
        :param surface:
        :return:
        """
        surface = normalize_entity_name(surface)
        try:
            bytestr = self.surface_index[surface]
            ids_array = array.array('d')
            ids_array.fromstring(bytestr)
            # print ('ids_array:\t', ids_array)
            result = []
            i = 0
            while i < len(ids_array) - 1:
                offset = ids_array[i]
                surface_score = ids_array[i + 1]
                entity = self._read_entity_from_offset(int(offset))
                # Check if the main name of the entity exactly matches the text.
                result.append((entity, surface_score))
                i += 2
            return result
        except KeyError:
            return []

    @staticmethod
    def _string_to_entity(line):
        """Instantiate entity from string representation.

        :param line:
        :return:
        """
        line = line.decode('utf-8')
        cols = line.strip().split('\t')
        mid = cols[0]
        name = cols[1]
        score = int(cols[2])
        aliases = cols[3:]
        return entity_linker.KBEntity(name, mid, score, aliases)

    def _read_entity_from_offset(self, offset):
        """Read entity string representation from offset.

        :param offset:
        :return:
        """
        self.entities_mm.seek(offset)
        l = self.entities_mm.readline()
        return self._string_to_entity(l)

    # 获取列表的第二个元素
    def get_indexrange_entity_el_pro_one_mention(self, mention, top_k=10):
        tuple_list = self.get_entities_for_surface(mention)
        entities_dict = dict()
        for entity, surface_score in tuple_list:
            entities_dict[entity.id] = surface_score
        entities_tuple_list = sorted(entities_dict.items(), key=lambda d:d[1], reverse=True)
        result_entities_dict = collections.OrderedDict()
        for i, (entity_id, surface_score) in enumerate(entities_tuple_list):
            i += 1
            result_entities_dict[entity_id] = surface_score
            if i >= top_k:
                break
        return result_entities_dict

if __name__ == '__main__':
    # get_aqqu_mids(fn_cwq_file.entity_list_file,fn_cwq_file.surface_map_file,fn_cwq_file.aqqu_entity_contained)
    # def get_aqqu_mids(entity_file, surface_file, aqqu_entityall_file):
    #     mids = set()
    #     with open(entity_file, 'r', encoding="utf-8") as f:
    #         mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    #         line = mm.readline()
    #         while line:
    #             cols = line.decode().strip().split('\t')
    #             mid = cols[0]
    #             mids.add(mid)
    #             line = mm.readline()
    #     with open(surface_file, 'r', encoding="utf-8") as f:
    #         for line in f:
    #             cols = line.rstrip().split('\t')
    #             mid = cols[2]
    #             mids.add(mid)
    #     write_set(mids, aqqu_entityall_file)
    # main()
    # logging.basicConfig(
    #     format='%(asctime)s : %(levelname)s : %(module)s : %(message)s', level=logging.INFO)
    # for entity, surface_score in (
    #     entity_linking_aqqu_index.get_entities_for_surface("taylor lautner")):  # Albert Einstein
    #     print(entity.id, surface_score)
    # for entity, surface_score in (entity_linking_aqqu_index.get_entities_for_surface('Agusan del Sur')):
    #     print(entity.id, surface_score)
    # mention_to_entities('Agusan del Sur', top_k=10)
    # print(mention_to_entities('2010 Formula One World Championship', top_k=10))
    # print(mention_to_entities('Theresa Russo', top_k=10))
    # 指定第二个元素排序
    # tuple_list.sort(key=takeSecond)
    # print('**************************')
    # for entity,surface_score in tuple_list:
    #     print(entity.id, surface_score)
    pass

