import matplotlib.pyplot as plt
import pm4py
import pandas
import warnings
warnings.simplefilter(action="ignore", category=pandas.errors.SettingWithCopyWarning)
from src.interaction_properties import get_interaction_patterns
from src.divergence_free_graph import get_divergence_free_graph
from src.oc_process_trees import load_from_pt




def keep_most_frequent_activities(relations, coverage):

    counts = relations.groupby("ocel:activity").apply(lambda frame:frame["ocel:eid"].nunique()).to_dict()
    shares = {key:value / (sum(counts.values())) for key,value in counts.items()}
    shares_sorted = list(reversed(sorted(shares.items(), key=lambda x:x[1])))
    cut_off =  min([i for i in range(len(shares_sorted)) if sum([entry[1] for entry in shares_sorted[:i]]) >= coverage])
    activities = [shares_sorted[i][0] for i in range(cut_off)]
    return relations[relations["ocel:activity"].isin(activities)]



def df2_miner_apply(log_path, activity_coverage):

    try:
        input_log = pm4py.read_ocel2(log_path).relations
    except:
        input_log = pm4py.read_ocel(log_path).relations

    #do any sort of preprocessing of the log here
    #strongly recommended, as no noise is filtered
    #typically, we remove infrequent activities
    input_log = keep_most_frequent_activities(input_log,activity_coverage)

    div, con, rel, defi = get_interaction_patterns(input_log)
    print("Interacting Properties Done")
    df2_graph = get_divergence_free_graph(input_log,div,rel)
    print("DF2 Graph Done")
    process_tree = pm4py.discover_process_tree_inductive(df2_graph)
    print("Traditional Process Tree Done")
    ocpt = load_from_pt(process_tree,rel,div,con,defi)
    print("Object-Centric Process Tree Done")
    return ocpt



