from common.hand_files import read_list, read_pickle, write_set
from datasets_interface.virtuoso_interface.freebase_sparql_odbc import SparqlQueryODBC
# from common.globals_args import schema_lines_list, property_reverse_dict
from collections import OrderedDict

sqlodbc = SparqlQueryODBC()

def sparql_execuate_compared_goldanswers(qid, sparql, gold_answers):
    '''execuation sparql'''
    results_dict = dict()
    gold_answer_id_set = set()
    for gold_answer in gold_answers:
        gold_answer_id_set.add(gold_answer['answer_id'])
    query_answers_id_set = execute_sparql(sparql)
    print (query_answers_id_set)

    is_equal = False
    if gold_answer_id_set & query_answers_id_set == gold_answer_id_set | query_answers_id_set:
        results_dict[qid] = 1
        is_equal = True
        print(('%s\t%d') % (qid, is_equal))
    else:
        results_dict[qid] = 0
        print(('%s\t%d\t%s\t%s') % (qid, is_equal, gold_answer_id_set, query_answers_id_set))

def execute_sparql(sparql):
    query_answers_id_set = sqlodbc.execute_sparql(sparql)
    return query_answers_id_set

def execute_sparql_two_args(sparql):
    sqlodbc.execute_sparql_two_args(sparqlquery=sparql)

def execute_sparql_three_args(sparql):
    sqlodbc.execute_sparql_three_args(sparqlquery=sparql)

def get_s_p_literal_none(literal_value):
    s_p = sqlodbc.get_s_p_literal_none(literal_value)
    return s_p

def get_s_p_literal_function(literal_value, literal_function, literaltype):
    s_p = sqlodbc.get_s_p_literal_function(literal_value, literal_function, literaltype)
    return s_p

def get_p_o_by_entity(entity):
    p_o_set, o_set, p1_set = sqlodbc.get_p_o(entity)
    return p_o_set, o_set, p1_set

def get_s_p_by_entity(entity):
    s_p_set, s_set, p2_set = sqlodbc.get_s_p(entity)
    return s_p_set, s_set, p2_set

def get_domain_by_property(property):
    # subject type
    sparql = 'SELECT DISTINCT ?object WHERE { :'\
             +property+' <http://www.w3.org/1999/02/22-rdf-syntax-ns#domain> ?object .}'
    domain_class_set = sqlodbc.execute_sparql(sparql)
    return domain_class_set

def get_range_by_property(property):
    '''object type'''
    sparql = 'SELECT DISTINCT ?object WHERE { :'+property\
             +' <http://www.w3.org/1999/02/22-rdf-syntax-ns#range> ?object .}'
    range_class_set = sqlodbc.execute_sparql(sparql)
    return range_class_set

def get_domain(property_str):
    # subject type
    # sparql = 'SELECT DISTINCT ?object WHERE { :'+property_str+' <http://www.w3.org/2000/01/rdf-schema#domain> ?object .}'
    sparql = 'SELECT DISTINCT ?object WHERE { :'+property_str+' :type.property.schema ?object .}'
    domains_set = sqlodbc.execute_sparql(sparql)
    return domains_set

def get_range(property_str):
    # object type
    # sparql = 'SELECT DISTINCT ?object WHERE { :'+property_str+' <http://www.w3.org/2000/01/rdf-schema#range> ?object .}'
    sparql = 'SELECT DISTINCT ?o WHERE { :'+property_str+' :type.property.expected_type ?o}'
    range_set = sqlodbc.execute_sparql(sparql)
    return range_set

def get_p_set(instance_str):
    sparql = 'SELECT DISTINCT ?p WHERE {:'+instance_str+' ?p ?o .}'
    return sqlodbc.execute_sparql(sparql)

def get_classes_of_instance(instance_str):
    # sparql = 'SELECT DISTINCT ?class WHERE {' \
    #          '{:' + instance_str + ' :type.object.type ?class .}' \
    #          'UNION ' \
    #          '{:' + instance_str + ' :common.topic.notable_types ?class}' \
    #          '}'
    sparql = 'SELECT DISTINCT ?class WHERE {' \
             ':' + instance_str + ' :type.object.type ?class .}'
    classes = sqlodbc.execute_sparql(sparql)
    return classes

def get_all_notable_types():
    '''common.topic.notable_types'''
    sparql = 'SELECT DISTINCT ?type WHERE {' \
            '?x :common.topic.notable_types ?type. }'
    notable_types = sqlodbc.execute_sparql(sparql)
    for notable_type in notable_types:
        print(notable_type)
    return notable_types

def get_classes_notable_types(instance_str):
    sparql = 'SELECT DISTINCT ?class WHERE {' \
             ':' + instance_str + ' :common.topic.notable_types ?class}'
    return sqlodbc.execute_sparql(sparql)

def get_all_classes_with_count():
    sparql = 'SELECT DISTINCT ?type WHERE {?type :type.object.type  :type.type .}'
    classes = sqlodbc.execute_sparql(sparql)
    # mid_class_set = set()
    human_class_set = set()
    human_class_with_names_dict = dict()
    error_class_list = []
    for class_str in classes:
        try:
            instance_count = get_instance_by_class(class_str)
            count = instance_count.pop()
            print(class_str, count)
            human_class_set.add(('%s\t%d') % (class_str, count))
        except Exception as e:
            error_class_list.append(class_str)
        # if class_str.startswith('m.'):
        #     mid_class_set.add(class_str)
        # else:
        #     try:
        #         print(class_str)
        #         class_names = sqlodbc.get_names(class_str)
        #         # class_alias_names = sqlodbc.get_alias_names(class_str)
        #         # class_names = class_names.union(class_alias_names)
        #         human_class_set.add(class_str)
        #         if len(class_names) > 0:
        #             human_class_with_names_dict[class_str] = class_names
        #         print(class_names)
        #     except Exception as e:
        #         print(('%s\t%d') % (class_str, -1))
        #         error_class_list.append(class_str)
    print(len(classes))
    write_set(human_class_set, './mid_class.txt')
    print(error_class_list)
    # write_dict(human_class_with_names_dict, './human_class_names.txt')

def get_all_classes():
    sparql = 'SELECT DISTINCT ?type WHERE {?type :type.object.type  :type.type .}'
    classes = sqlodbc.execute_sparql(sparql)
    # mid_class_set = set()
    human_class_set = set()
    human_class_with_names_dict = dict()
    error_class_list = []
    for class_str in classes:
        print (class_str)
        human_class_set.add(class_str)
        # if class_str.startswith('m.'):
        #     mid_class_set.add(class_str)
        # else:
        #     try:
        #         print(class_str)
        #         class_names = sqlodbc.get_names(class_str)
        #         # class_alias_names = sqlodbc.get_alias_names(class_str)
        #         # class_names = class_names.union(class_alias_names)
        #         human_class_set.add(class_str)
        #         if len(class_names) > 0:
        #             human_class_with_names_dict[class_str] = class_names
        #         print(class_names)
        #     except Exception as e:
        #         print(('%s\t%d') % (class_str, -1))
        #         error_class_list.append(class_str)
    print(len(classes))
    write_set(human_class_set, './mid_class.txt')
    print (error_class_list)
    # write_dict(human_class_with_names_dict, './human_class_names.txt')

def get_all_class_names():

    def write_dict(dict, write_file):
        fi = open(write_file, "w", encoding="utf-8")
        # fi.write(str(len(dict)))
        # fi.write("\n")
        for key in dict:
            fi.write(str(key))
            fi.write("\t")
            fi.write(str(dict[key]))
            fi.write("\n")
        fi.close()

    # human_types_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_types')
    human_types_list = read_list('./freebase_types')
    error_qid_list = []
    name_to_class_dict = OrderedDict()
    for i, line in enumerate(human_types_list):
        try:
            names = get_names(line)
            if len(names) > 0:
                name = names.pop().lower()
                if name in name_to_class_dict:
                    name_to_class_dict[name][line] = 1.0
                else:
                    class_dict = dict()
                    class_dict[line] = 1.0
                    name_to_class_dict[name] = class_dict
                print (i, name)
                # token_list = name.lower().split(' ')
                # print(('%s\t%s') % (line, '\t'.join(token_list)))
        except Exception as e:
            error_qid_list.append(line)
        # if line not in human_types_list:
        #     print(line)
    print('#error:\t', error_qid_list)
    write_dict(name_to_class_dict, './types_reverse.txt')

    # ['user.joram.environmental_science_$0026_technology.water_quality',
    #  'user.rogopag.www$002ecittadiivrea$002ecom.topic', 'user.player.player_entertainment_group_inc$002e.branding',
    #  'user.sankeerth.http$003a$002f$002fwebisee$002ecom.topic',
    #  'user.player.player_entertainment_group_inc$002e.televisions_production',
    #  'user.player.player_entertainment_group_inc$002e.visual_art', 'user.robert.world$0027s_tallest.topic',
    #  'user.rial13.dre_$0022rial$0022_porcher.topic', 'user.ray315.$0432$0430$043b$044e$0442$0430.topic',
    #  'user.bluenorthernmusic.musical_artist$002c_music_lessons.topic',
    #  'user.mad_god.$0418$0441$043a$0443$0441$0441$0442$0432$0435$043d$043d$044b$0439_$0438$043d$0442$0435$043b$043b$0435$043a$0442.topic',
    #  'user.player.player_entertainment_group_inc$002e.games', 'user.dreig.web_3$002e0.topic',
    #  'user.beatyourprice.http$003a$002f$002fwww$002ebeatyourprice$002ecom.topic',
    #  'user.brabblejr.www$002ebrabble$002ccom.topic', 'user.player.player_entertainment_group_inc$002e.concerts',
    #  'user.player.player_entertainment_group_inc$002e.media_common', 'user.shomoa.magic$003a_the_gathering.subtype',
    #  'user.mad_god.$0418$0441$043a$0443$0441$0441$0442$0432$0435$043d$043d$044b$0439_$0438$043d$0442$0435$043b$043b$0435$043a$0442.ai',
    #  'user.shomoa.magic$003a_the_gathering.color', 'user.gadgetsgalore.www$002er4us$002ecom$002ftrophy.topic',
    #  'user.player.player_entertainment_group_inc$002e.film', 'user.robert.world$0027s_tallest.building',
    #  'user.shomoa.magic$003a_the_gathering.x_type', 'user.xiongy.$4e2d$56fd.x', 'user.hsetty.web2$002e0.topic',
    #  'user.rogopag.robanostra$002ehomeftp$002enet.topic', 'user.freedom2002.$00e2$1ea11ea1c.topic',
    #  'user.integrity19.taxation_and_pornography$003a_designing_system_to_survive_constitutional_challenges.topic',
    #  'user.visha.$0645$062d$0645$062f_$062d$0645$06cc$062f_$0634$0627$06be$062f.topic',
    #  'user.shomoa.magic$003a_the_gathering.card',
    #  'user.player.player_entertainment_group_inc$002e.entertainment_company',
    #  'user.rrhobbs.location_scouting$002c_location_management_and_locations_for_film$002c_tv$002c_photo_and_events.topic',
    #  'user.player.player_entertainment_group_inc$002e.topic', 'user.shomoa.magic$003a_the_gathering.supertype',
    #  'user.paulsipot.www$002eunnamedservice$002ecom.topic', 'user.shomoa.magic$003a_the_gathering.topic',
    #  'user.zameen.ringtones$002emobi.topic',
    #  'user.archbishopderrickyoung.archbishop_derrick_l$002e_young_d$002ed$002e$002c_d$002emin$002e.topic',
    #  'user.player.player_entertainment_group_inc$002e.computer_game_designer', 'user.xiongy.$4e2d$56fd.topic',
    #  'user.shomoa.magic$003a_the_gathering.zone', 'user.player.player_entertainment_group_inc$002e.product_integration',
    #  'user.saranshsehgal.www$002emcllo$002ecom.topic', 'user.funkyflash.www$002edujdc$002eorg.topic',
    #  'user.player.player_entertainment_group_inc$002e.game_development',
    #  'user.player.player_entertainment_group_inc$002e.tv_program',
    #  'user.chiliteslegacy.default_domain.the_chi_lites_bass_singer_creadel_jones_had_a_son_darren_in_which_played_a_important_role_in_helping_protect_his_legacy_against_fraud_exploition_and_embelzelments_to_creadel_jones_singer_legacy_and_his_music_his_son_darren_cubie_has_been_a_force_of_truth_and_guidence_for_iconic_legacies_an_thier_futher_darren_has_made_wed_sites_for_the_news_of_legacy_through_out_the_entertainment_field_that_mistreated_by_abuse_and_for_news_related_and_music_to_legendary_artist_icons_and_music_called_http_www_chilites_ning_com_and_http_www_chilites_net_all_are_real_disscussion_stating_information_music_abuse_and_news_and_music_creadel_jones_family_includes_wife_deborah_jones_and_two_sisters',
    #  'user.joram.environmental_science_$0026_technology.topic',
    #  'user.player.player_entertainment_group_inc$002e.computer_games',
    #  'user.mirzak2.www$002emirzak2$002ewebs$002ecom.topic', 'user.pasidor.pasidor$002ecom.topic',
    #  'user.imteam1.http$003a$002f$002fwww$002egreenconservationproducts$002ecom$002f.topic',
    #  'user.player.player_entertainment_group_inc$002e.arts_entertainment',
    #  'user.rogopag.www$002enastypixel$002ecom.topic',
    #  'user.kunninmindzradio.http$003a$002f$002fkunninmindz$002ecom.topic']

def get_names(instance_str):
    # alias = sqlodbc.get_alias_names(instance_str)
    # names = names.union(alias)
    # ?x0: common.topic.alias ?name.
    return sqlodbc.get_names(instance_str)

def get_alias(instance_str):
    return sqlodbc.get_alias_names(instance_str)

def get_all_instances():
    sparql = "SELECT DISTINCT ?instance ?name WHERE{" \
             "?instance :type.object.type ?type." \
             "?type :type.object.type :type.type." \
             "?instance :type.object.name ?name. " \
             "FILTER(langMatches(lang(?name), 'en')).}"
    instances_count = sqlodbc.execute_sparql_two_args(sparql)

def get_s_o_by_property(property_str):
    # sparql = 'SELECT DISTINCT ?s WHERE {?s :'+property_str+' ?o .}'
    sparql = 'SELECT count(DISTINCT ?s) WHERE {?s :'+property_str+' ?o .}'
    answers = sqlodbc.execute_sparql(sparql)
    return answers.pop()

def get_instance_properties_by_class(class_str):
    sparql = 'SELECT DISTINCT ?o WHERE {:'+class_str+' :type.type.instance ?o .}'
    instances = sqlodbc.execute_sparql(sparql)
    related_properties_set = set()
    for instance in instances:
        related_properties_set.add(get_p_set(instance_str=instance))
    return related_properties_set

def get_instance_by_class(class_str):
    # sparql = 'SELECT DISTINCT ?o WHERE {' \
    #          '{:'+class_str+' :type.type.instance ?o .}' \
    #          'UNION ' \
    #          '{?o :common.topic.notable_types :'+class_str+'}' \
    #          '}'
    sparql = 'SELECT count(DISTINCT ?instance) WHERE {' \
               '?instance :type.object.type :'+class_str+'.}'
    instances_set = sqlodbc.execute_sparql(sparql)
    return instances_set

def get_instance_by_class_notable_type(class_str):
    sparql = 'SELECT DISTINCT ?instance WHERE {' \
             '?instance :common.topic.notable_types :'+class_str+'}'
    return sqlodbc.execute_sparql(sparql)

def get_all_properties():
    sparql = 'SELECT DISTINCT ?relation WHERE { ?relation :type.object.type  :type.property .}'
    properties = sqlodbc.execute_sparql(sparql)
    for property in properties:
        print (property)

def get_all_properties_with_count():
    sparql = 'SELECT DISTINCT ?relation WHERE { ?relation :type.object.type  :type.property .}'
    properties = sqlodbc.execute_sparql(sparql)
    properties_with_count_list = []
    error_property_list = []
    for property in properties:
        # print(property)
        try:
            instances_count = get_s_o_by_property(property)
            print(property, instances_count)
            properties_with_count_list.append(('%s\t%d') % (property, instances_count))
        except Exception as e:
            print('#error!!!', property)
            error_property_list.append(property)
    print(len(properties))
    write_set(properties_with_count_list, './properties_with_count.txt')
    print(error_property_list)

def get_properties_with_domain_range():
    sparql = 'SELECT DISTINCT ?relation WHERE {' \
             '?relation :type.object.type  :type.property .}'
    properties = sqlodbc.execute_sparql(sparql)
    mid_property_set = set()
    human_property_set = set()
    # human_property_domain_range_dict = dict()
    human_property_with_names_dict = dict()
    error_property_list = []
    for property in properties:
        # sparql = '''SELECT count(?s) WHERE {
        # ?s :'''+property+''' ?o
        # }'''
        try:
            # count = execute_sparql(sparql)
            property_domain = get_domain(property)
            property_range = get_range(property)
            print(('%s\t%s\t%s') % (property, str(list(property_domain)),
                                    str(list(property_range))))
        except Exception as e:
            error_property_list.append(property)
        # if property.startswith('m.'):
        #     mid_property_set.add(property)
        # else:
        #     try:
        #         human_property_set.add(property)
        #         # domain_set = get_domain(property)
        #         # range_set = get_range(property)
        #         # print(property, domain_set, range_set)
        #         # human_property_domain_range_dict[property] = (domain_set, range_set)
        #         property_names = sqlodbc.get_names(property)
        #         # class_alias_names = sqlodbc.get_alias_names(class_str)
        #         # class_names = class_names.union(class_alias_names)
        #         if len(property_names) > 0:
        #             human_property_with_names_dict[property] = property_names
        #     except Exception as e:
        #         error_property_list.append(property)
        # s_count = get_s_o_by_property(property)
        # if s_count > 0:
        #     print(('%s\t%d') % (property, s_count))
    # print(len(properties))
    # print(len(mid_property_set))
    # print(len(human_property_set))
    print(error_property_list)
    # write_set(mid_property_set, './mid_property.txt')
    # write_set(human_property_set, './human_property.txt')
    # write_dict(human_property_domain_range_dict, './human_property_domain_range.txt')
    # write_dict(human_property_with_names_dict, './human_property_names.txt')

def mediator_to_instances():
    mediators_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/mediators.tsv')
    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.04.10_freebase_mediators_instance_sp.txt', sys.stdout)
    error_qid_list = []

    for i, line in enumerate(mediators_list):
        if line in ['common.notable_for', 'medicine.drug_label_section',
                    'location.geocode', 'film.performance',
                    'measurement_unit.dated_percentage', 'base.schemastaging.nutrition_information',
                    'common.webpage', 'music.track_contribution', 'measurement_unit.dated_integer']:
            continue
        try:
            sparql = '''SELECT DISTINCT ?s ?p ?instance WHERE {
            ?s ?p ?instance  . 
            ?instance :type.object.type :'''+line+'''
            }'''
            execute_sparql_three_args(sparql, line)

            # instances = get_instance_by_class(line)
            # for instance in instances:
            #     p_o_set, _, _ = get_p_o_by_entity(instance)
            #     for p_o in p_o_set:
            #         print(('%d\t%s\t%s') % (i, instance, p_o))

        except Exception as e:
            error_qid_list.append(line)
        # if line not in human_types_list:
        #     print(line)
    print(error_qid_list)

def type_to_instances():
    # mediators_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/mediators.tsv')
    human_types_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_types')

    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.03.15_freebase_instance_type_1.txt', sys.stdout)
    error_qid_list = []

    filter_list_3 = ['music.recording', 'music.release_track',
                   'base.type_ontology.abstract', 'base.type_ontology.non_agent',
                   'common.notable_for', 'common.topic']
    filter_list_2 = ['type.content_import', 'type.content', 'type.namespace', 'common.document',
                     'base.type_ontology.agent', 'base.type_ontology.inanimate', 'base.type_ontology.animate']

    filter_list_4 = ['user.joram.environmental_science_$0026_technology.water_quality', 'user.rogopag.www$002ecittadiivrea$002ecom.topic',
                     'user.player.player_entertainment_group_inc$002e.branding', 'user.sankeerth.http$003a$002f$002fwebisee$002ecom.topic',
                     'user.player.player_entertainment_group_inc$002e.televisions_production',
                     'user.player.player_entertainment_group_inc$002e.visual_art', 'user.robert.world$0027s_tallest.topic',
                     'user.rial13.dre_$0022rial$0022_porcher.topic', 'user.ray315.$0432$0430$043b$044e$0442$0430.topic',
                     'user.bluenorthernmusic.musical_artist$002c_music_lessons.topic',
                     'user.mad_god.$0418$0441$043a$0443$0441$0441$0442$0432$0435$043d$043d$044b$0439_$0438$043d$0442$0435$043b$043b$0435$043a$0442.topic',
                     'user.player.player_entertainment_group_inc$002e.games', 'user.dreig.web_3$002e0.topic',
                     'user.beatyourprice.http$003a$002f$002fwww$002ebeatyourprice$002ecom.topic', 'user.brabblejr.www$002ebrabble$002ccom.topic',
                     'user.player.player_entertainment_group_inc$002e.concerts', 'user.player.player_entertainment_group_inc$002e.media_common',
                     'user.shomoa.magic$003a_the_gathering.subtype', 'user.mad_god.$0418$0441$043a$0443$0441$0441$0442$0432$0435$043d$043d$044b$0439_$0438$043d$0442$0435$043b$043b$0435$043a$0442.ai',
                     'user.shomoa.magic$003a_the_gathering.color', 'user.gadgetsgalore.www$002er4us$002ecom$002ftrophy.topic',
                     'user.player.player_entertainment_group_inc$002e.film', 'user.robert.world$0027s_tallest.building',
                     'user.shomoa.magic$003a_the_gathering.x_type', 'user.xiongy.$4e2d$56fd.x',
                     'user.hsetty.web2$002e0.topic', 'user.rogopag.robanostra$002ehomeftp$002enet.topic',
                     'user.freedom2002.$00e2$1ea11ea1c.topic', 'user.integrity19.taxation_and_pornography$003a_designing_system_to_survive_constitutional_challenges.topic',
                     'user.visha.$0645$062d$0645$062f_$062d$0645$06cc$062f_$0634$0627$06be$062f.topic',
                     'user.shomoa.magic$003a_the_gathering.card', 'user.player.player_entertainment_group_inc$002e.entertainment_company',
                     'user.rrhobbs.location_scouting$002c_location_management_and_locations_for_film$002c_tv$002c_photo_and_events.topic',
                     'user.player.player_entertainment_group_inc$002e.topic', 'user.shomoa.magic$003a_the_gathering.supertype',
                     'user.paulsipot.www$002eunnamedservice$002ecom.topic', 'user.shomoa.magic$003a_the_gathering.topic',
                     'user.zameen.ringtones$002emobi.topic', 'user.archbishopderrickyoung.archbishop_derrick_l$002e_young_d$002ed$002e$002c_d$002emin$002e.topic',
                     'user.player.player_entertainment_group_inc$002e.computer_game_designer', 'user.xiongy.$4e2d$56fd.topic',
                     'user.shomoa.magic$003a_the_gathering.zone', 'user.player.player_entertainment_group_inc$002e.product_integration',
                     'user.saranshsehgal.www$002emcllo$002ecom.topic', 'user.funkyflash.www$002edujdc$002eorg.topic',
                     'user.player.player_entertainment_group_inc$002e.game_development', 'user.player.player_entertainment_group_inc$002e.tv_program',
                     'user.chiliteslegacy.default_domain.the_chi_lites_bass_singer_creadel_jones_had_a_son_darren_in_which_played_a_important_role_in_helping_protect_his_legacy_against_fraud_exploition_and_embelzelments_to_creadel_jones_singer_legacy_and_his_music_his_son_darren_cubie_has_been_a_force_of_truth_and_guidence_for_iconic_legacies_an_thier_futher_darren_has_made_wed_sites_for_the_news_of_legacy_through_out_the_entertainment_field_that_mistreated_by_abuse_and_for_news_related_and_music_to_legendary_artist_icons_and_music_called_http_www_chilites_ning_com_and_http_www_chilites_net_all_are_real_disscussion_stating_information_music_abuse_and_news_and_music_creadel_jones_family_includes_wife_deborah_jones_and_two_sisters',
                     'user.joram.environmental_science_$0026_technology.topic', 'user.player.player_entertainment_group_inc$002e.computer_games',
                     'user.mirzak2.www$002emirzak2$002ewebs$002ecom.topic', 'user.pasidor.pasidor$002ecom.topic',
                     'user.imteam1.http$003a$002f$002fwww$002egreenconservationproducts$002ecom$002f.topic',
                     'user.player.player_entertainment_group_inc$002e.arts_entertainment', 'user.rogopag.www$002enastypixel$002ecom.topic',
                     'user.kunninmindzradio.http$003a$002f$002fkunninmindz$002ecom.topic']

    for line in human_types_list:
        if line in filter_list_2 or line in filter_list_3 or line in filter_list_4: continue
        try:
            instances = get_instance_by_class(line)
            for instance in instances:
                print(('%s\t%s') % (line, instance))
        except Exception as e:
            error_qid_list.append(line)
        # if line not in human_types_list:
        #     print(line)
    print(error_qid_list)

def instance_to_types():
    instance_to_types_dict = dict()
    types_instance_list = read_list('./2019_03_15_freebase_instance_type_1')
    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.03.20_freebase_instance_type_1_reverse.txt', sys.stdout)

    for i, line in enumerate(types_instance_list):
        terms = line.split('\t')
        type_str = terms[0]
        instance = terms[1]
        if instance in instance_to_types_dict.keys():
            instance_to_types_dict[instance].add(type_str)
        else:
            types = set()
            types.add(type_str)
            instance_to_types_dict[instance] = types
    for instance, types in instance_to_types_dict.items():
        print(('%s\t%s') % (instance, str(types)))

def notable_type_to_instances():

    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.03.15_freebase_instance_notable_1.txt', sys.stdout)

    error_qid_list = []
    notable_types_types_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_notable_types')
    for line in notable_types_types_list:
        try:
            instances = get_instance_by_class_notable_type(line)
            for instance in instances:
                print(('%s\t%s') % (line, instance))
        except Exception as e:
            error_qid_list.append(line)
        # if line not in human_types_list:
        #     print(line)
    print(error_qid_list)

def get_all_reverse_properties():
    sparql = 'PREFIX : <http://rdf.freebase.com/ns/> ' \
             'SELECT ?s ?o WHERE { ?s :type.property.reverse_property ?o}'
    execute_sparql_two_args(sparql)

def get_numerical_properties():
    numerical_property_tuple_list = []
    #type datatime
    sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT distinct ?p WHERE ' \
             '{ ?p :type.property.expected_type :type.datetime.}'
    properties = execute_sparql(sparql)
    for property in properties:
        numerical_property_tuple_list.append((property, 'type.datatime'))

    #type float
    sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT distinct ?p WHERE {' \
             ' ?p :type.property.expected_type :type.float.}'
    properties = execute_sparql(sparql)
    for property in properties:
        numerical_property_tuple_list.append((property, 'type.float'))

    #type int
    sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT distinct ?p WHERE {' \
             ' ?p :type.property.expected_type :type.int.}'
    properties = execute_sparql(sparql)
    for property in properties:
        numerical_property_tuple_list.append((property, 'type.int'))

    #type.enumeration
    sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT distinct ?p WHERE {' \
             ' ?p :type.property.expected_type :type.enumeration.}'
    properties = execute_sparql(sparql)
    for property in properties:
        numerical_property_tuple_list.append((property, 'type.enumeration'))

    for i, (property, property_expected_type) in enumerate(numerical_property_tuple_list):
        print(('%s\t%s') % (property, property_expected_type))
        # sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT count(distinct ?s) WHERE { ?s :'+property+' ?o.}'
        # count_property = kb_interface.execute_sparql(sparql)
        # print(('%s\t%s\t%s') % (property, property_expected_type, count_property))

def get_all_relation_names():
    human_relation_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_relations')
    error_qid_list = []
    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.03.18_freebase_relation_finalwords.txt', sys.stdout)

    for line in human_relation_list:
        try:
            # sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT count(distinct ?s) WHERE { ?s :'+line+' ?o}'
            # count_relation = kb_interface.execute_sparql(sparql)
            # print(('%s\t%d') % (line, count_relation.pop()))
            names = get_names(line)
            if len(names) > 0:
                name = names.pop()
                token_list = name.lower().split(' ')
                print(('%s\t%s') % (line, '\t'.join(token_list)))
        except Exception as e:
            error_qid_list.append(line)
        # if line not in human_types_list:
        #     print(line)
    print(error_qid_list)

def get_all_relation_domain_range():
    human_relation_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_relations')
    error_qid_list = []
    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.03.20_freebase_relation_domain_range.txt', sys.stdout)

    for line in human_relation_list:
        try:
            domains_set = get_domain(line)
            range_set = get_range(line)
            print(('%s\t%s\t%s') % (line, list(domains_set), list(range_set)))

            # sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT count(distinct ?s) WHERE { ?s :'+line+' ?o}'
            # count_relation = kb_interface.execute_sparql(sparql)
            # print(('%s\t%d') % (line, count_relation.pop()))
            # names = kb_interface.get_names(line)
            # if len(names) > 0:
            #     name = names.pop()
            #     token_list = name.lower().split(' ')
            #     print(('%s\t%s') % (line, '\t'.join(token_list)))
        except Exception as e:
            error_qid_list.append(line)
        # if line not in human_types_list:
        #     print(line)
    print(error_qid_list)

def get_freebase_schema():
    import sys
    from parsing.logger_test import Logger
    sys.stdout = Logger('./2019.05.13_freebase_schema.txt', sys.stdout)
    # types_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_types')
    # mediators = read_list('../dataset/resources_cwq/dataset_freebase_latest/mediators.tsv')
    # relation_domain_range_list = read_list('../dataset/resources_cwq/dataset_freebase_latest/freebase_relations_domain_range')
    types_list = read_list('./20190512_ywsun/75_all_classes.txt')
    mediators = read_list('./20190512_ywsun/mediators.tsv')
    relation_domain_range_list = read_list('./20190512_ywsun/2019.05.12_properties_with_domain_range.txt')

    relation_domain_range_tuple_list = []
    for relation_domain_range in relation_domain_range_list:
        cols = relation_domain_range.split('\t')
        relation = cols[0]
        domains_list = eval(cols[1])
        ranges_list = eval(cols[2])
        relation_domain_range_tuple_list.append((relation, domains_list, ranges_list))

    for type_ in types_list:
        attr = 'main'
        if type_ in mediators:
            attr = 'mediator'
        related_relation_range_list = []
        for i, (relation, domains_list, ranges_list) in \
                enumerate(relation_domain_range_tuple_list):
            if type_ in domains_list:
                related_relation_range_list.append((relation, ranges_list))
        for related_relation_range in related_relation_range_list:
            range = ''
            if len(related_relation_range[1]) > 0:
                range = related_relation_range[1][0]
            if len(related_relation_range[1]) > 1:
                print('error!!!', related_relation_range)
            print(('%s\t%s\t%s\t%s') % (type_,attr, related_relation_range[0], range))

def get_type_by_instance(instance):
    import mmap
    def _read_dict(pathfile):
        diction = dict()
        i = 0
        with open(pathfile, 'r', encoding='utf-8') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                cols = line.decode().strip().split('\t')
                diction[cols[0]] = eval(cols[1])
                line = mm.readline()
                print (i)
                i += 1
        mm.close()
        f.close()
        return diction

    # instance_types_dict = _read_dict('../dataset/resources_cwq/dataset_freebase_latest/freebase_instance_types_1')
    instance_types_dict = read_pickle('../dataset/resources_cwq/dataset_freebase_latest/freebase_instance_types_1.pickle')
    if instance in instance_types_dict:
        print(instance_types_dict[instance])
    print(len(instance_types_dict))
    # write_pickle(instance_types_dict, file_path='./freebase_instance_types_1.pickle')

def get_quotation_instance():
    # import sys
    # from parsing.logger_test import Logger
    # sys.stdout = Logger('./2019.03.22_quotation.txt', sys.stdout)

    sparql = 'PREFIX : <http://rdf.freebase.com/ns/> SELECT distinct ?s WHERE { ?s :type.object.type :media_common.quotation.}'
    instances = execute_sparql(sparql)
    for instance in instances:
        names = get_names(instance)
        if len(names) > 0:
            print (('%s\t%s') % (instance, names.pop()))

def get_properties_from_schema_by_type(type_, col_index=0):
    '''col_index=0: domain; col_index = 3: range'''
    properties = []
    # schema_file_path = '../dataset/resources_cwq/dataset_freebase_latest/freebase_schema'
    # schema_lines_list = read_list(schema_file_path)
    for schema_line in schema_lines_list:
        cols = schema_line.split('\t')
        if len(cols) <= col_index: continue
        if type_ == cols[col_index]:
            properties.append(cols[2])
    return properties

def is_mediator_from_schema(type_):
    result = False
    for schema_line in schema_lines_list:
        cols = schema_line.split('\t')
        if type_ == cols[0] and 'mediator' == cols[1]:
            result = True
    return result

def get_reverse_property_from_lexcion(property):
    '''get reverse property'''
    reverse_property = ''
    if property in property_reverse_dict.keys():
        reverse_property = property_reverse_dict[property][0]
    for key, value in property_reverse_dict.items():
        if key == property: reverse_property = value[0]
        if value[0] == property: reverse_property = key
    return reverse_property

def is_mediator_property_from_schema(property):
    result = False
    for schema_line in schema_lines_list:
        cols = schema_line.split('\t')
        if property == cols[2] and 'mediator' == cols[1]:
            result = True
    return result

def is_mediator_property_reverse_from_schema(property):
    '''property is a reverse mediator edge'''
    reverse_property = get_reverse_property_from_lexcion(property)
    is_reverse_mediator = is_mediator_property_from_schema(reverse_property)
    return is_reverse_mediator

def get_domain_range_from_schema_by_property(property):
    domain_range_tuple_list = []
    # schema_file_path = '../dataset/resources_cwq/dataset_freebase_latest/freebase_schema'
    # schema_lines_list = read_list(schema_file_path)
    for schema_line in schema_lines_list:
        cols = schema_line.split('\t')
        if len(cols) > 3 and property == cols[2]:
            domain_range_tuple_list.append((cols[0], cols[3]))
    return domain_range_tuple_list


from common.hand_files import read_set

if __name__ == "__main__":

    # names = kb_interface.get_names('m.04ygk0')
    # print (names)
    # sparqlquery = 'SELECT DISTINCT ?s WHERE { ?s ?p ?o } limit 10 '
    # query_answers_id_set = freebase_kb_interface.execute_sparql(sparqlquery)
    # print (query_answers_id_set)

    # import sys
    # from unit_test.logger_test import Logger
    # sys.stdout = Logger('./2019.07.05_denotation_names.log', sys.stdout)

    # instance_str = 'en.jamarcus_russell'
    union_all_denotations = read_set('./uniondenotation.txt')
    for i, denotation in enumerate(union_all_denotations):
        labels = get_names(instance_str=denotation)
        # name = ''
        # if len(labels) > 0:
        #     name = labels.pop()
        print(('%d\t%s\t%s') % (i, denotation, str(labels)))

    # import sys
    # from parsing.logger_test import Logger
    # sys.stdout = Logger('./2019.05.13_class_name.txt', sys.stdout)

    # kb_interface.get_all_reverse_properties()

    # kb_interface.get_all_classes()

    # kb_interface.get_all_classes_with_count()

    # kb_interface.get_all_properties()

    # kb_interface.get_properties_with_domain_range()

    # kb_interface.get_freebase_schema()

    # kb_interface.get_all_class_names()

    # kb_interface.get_all_properties_with_count()

    # sparql = '''
    # SELECT ?x0 ?name WHERE {
    #     ?x0 :type.object.type :common.topic.
    #     ?x0 :type.object.name ?name .
    #     FILTER (langMatches(lang(?name), 'en')).
    # }
    # '''

    # sparql = '''
    #     SELECT ?x1 ?p1 ?o1 ?p2 ?o2 WHERE {
    #     ?x1 :type.object.type :common.topic.
    #     ?o2 :type.object.type :common.topic.
    #     ?o1 :type.object.type :common.topic.
    #     ?x1 ?p1 ?o1. ?o1 ?p2 ?o2.
    #     FILTER (?x1 != ?o2)
    #     FILTER (!isLiteral(?o1))
    #     FILTER (?p1 != :type.object.type)
    #     FILTER (?p2 != :type.object.type)
    #     FILTER (?p1 != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    #     FILTER (?p2 != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
    # }
    # '''

    # sparql = '''
    #     SELECT ?x1 WHERE {
    #     ?x1 :type.object.type :common.topic.
    #     ?x1 ?p1 ?o1. ?o1 ?p2 ?o2.
    # } limit 10
    # '''
    # sqlodbc.execute_sparql_five_arg(sparqlquery=sparql)

    # s_p_set = sqlodbc.get_s_p_literal_none('\'2.32\'') # string
    # s_p_set = sqlodbc.get_s_p_literal_none('"1805"^^xsd:dateTime')  #type.datetime
    # s_p_set = sqlodbc.get_s_p_literal_none('"356.72"')  #float
    # s_p_set = sqlodbc.get_s_p_literal_none("'2009'^^xsd:dateTime")  #datetime
    # s_p_set = get_s_p_literal_none("\"\"1961\"^^xsd:dateTime\"")
    # for s_p in s_p_set:
    #     print (s_p)
    # print (len(s_p_set))
    # get_properties()
    # mediator_to_instances()
    # get_all_classes()
    # get_properties()
    # get_all_instances()
    # names = get_names('m.0h_09qp')
    # name = names.pop()
    # print (name.encode('utf-8').decode('latin1'))
    # from datasets_interface.dataset_interface_helper import convert_luan_to_chinese, convert_question_to_question
    # name = convert_question_to_question(name.encode('utf-8'))

    # from common.globals_args import fn_cwq_file as fn
    # entity_types = read_pickle(fn.entity_types_file_dat)
    # error_instance_list = set()
    # for entity in entity_types.keys():
    #     try:
    #         names = get_names(entity) #'m.010cgztd'
    #         if len(names) > 0:
    #             print(('%s\t%s') % (entity, names))
    #     except Exception as e:
    #         error_instance_list.add(entity)
    # print('#error:', error_instance_list)

    # get_properties()
    # lines = read_list('./2019_03_14_freebase_instance')
    # for instance_str in lines:
    #     classes = get_classes(instance_str=instance_str)
    #     print(('%s\t%s') % (instance_str, '\t'.join(classes)))

    # sparql="SELECT (COUNT(?x0) AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \n?x0 :type.object.type :computer.computing_platform . \nVALUES ?x1 { :en.portable_document_format } \n?x1 :computer.file_format.used_on ?x0 . \nFILTER ( ?x0 != ?x1  )\n}\n}"
    # sparql="SELECT (?x0 AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \nVALUES ?x1 { :en.lascaux } .\n?x0:type.object.type :base.biblioness.bibs_location .\n?x1 :base.caveart.cave.region ?x0 .\nFILTER ( ?x1 != ?x0 ) .\n}\n}"
    # sparql="SELECT (?x0 AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \nVALUES ?x1 { :en.mount_rushmore } .\nVALUES ?x2 { :en.nancy_hanks } .\n?x0:type.object.type :government.political_appointer .\n?x1 :visual_art.artwork.art_subject ?x0 .\n?x2 :people.person.children ?x0 .\nFILTER ( ?x1 != ?x2 && ?x1 != ?x0 && ?x2 != ?x0 ) .\n}\n}\n"
    # answers_entities = sqh.execute_sparql(sparql)
    # entities_names = sqh.get_names(answers_entities)

    # sparql = "SELECT ((?x0) AS ?value) WHERE {\nSELECT DISTINCT ?x0  WHERE { \n?x0 :type.object.type :computer.computing_platform . \nVALUES ?x1 { :en.portable_document_format } \n?x1 :computer.file_format.used_on ?x0 . \nFILTER ( ?x0 != ?x1  )\n}\n}"
    # sqh.execute_sparql(sparql)
    #     sparql="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX : <http://rdf.freebase.com/ns/>
    # SELECT (?x0 AS ?value) WHERE {
    # SELECT DISTINCT ?x0  WHERE {
    # ?x0 :type.object.type :music.release_track .
    # {
    # SELECT (MIN(?y1) AS ?x1)  WHERE {
    # ?y0 :type.object.type :music.release_track .
    # VALUES ?y2 { :m.03b7wt1 }
    # ?y0 :music.release_track.track_number ?y1 .
    # ?y2 :music.release.track_list ?y0 .
    # FILTER ( ?y0 != ?y1 && ?y0 != ?y2 && ?y1 != ?y2  )
    # }
    # }
    # VALUES ?x2 { :m.03b7wt1 }
    # ?x0 :music.release_track.track_number ?x1 .
    # ?x2 :music.release.track_list ?x0 .
    # FILTER ( ?x0 != ?x1 && ?x0 != ?x2 && ?x1 != ?x2  )
    # }
    # }
    # """
    #     sqo=SparqlQueryODBC()
    #     answers = sqo.execute_sparql(sparql)

