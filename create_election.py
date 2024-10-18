from .digital_id import *
from .vote import *
import json 
import random
import os 
from collections import defaultdict

states = []
def main():
    global states
    with open("./election/counties.json", "r") as f:
        states = json.load(f)

    candidates = ["howard", "raj", "sheldon", "leonard"]
    # create_votes(states, candidates)
    root_dir = "./election/data/us"
    # validate_election(root_dir)
    # print("election has been validated")
    # verify_election(root_dir)
    # print("election has been verified")
    winner = get_results(root_dir)
    print(f"Winner of the election: {winner}")

def get_results(root_dir):
    results = get_results_rec(root_dir)
    counts = defaultdict(int)
    for r in results:
        counts[r] += 1 
    winner = results[0]
    for count in counts:
        if counts[winner] <= counts[count]:
            winner = count 
    return winner

def get_results_rec(root_dir):

    sub_directories = get_sub_directories(root_dir)
    if len(sub_directories) == 0:
        return -1
    children = []
    for sub in sub_directories:
        children.append(get_results_rec(sub))
    if len(children) == 2 and children[0] == -1:
        vd = VoteData.load(root_dir + "/vote/vote.vd")
        return [vd.candidate]
    ret = [item for child in children for item in child ]
    return ret


    

def validate_election(root_dir):
    
    build_tree(root_dir, True)

def verify_election(root_dir):
    build_tree(root_dir, False)

def get_sub_directories(directory_path):
    return [os.path.join(directory_path, d) for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

def load_vote_block(root_dir):
    subs = get_sub_directories(root_dir)
    votes = []
    for d in subs:
        votes.append(Vote.load_vote(d + "/vote/"))
    return VoteBlock(votes)
        



def build_tree(root_dir, validate):
    sub_directories = get_sub_directories(root_dir)
    if len(sub_directories) == 0:
        return -1
    children = []
    for sub in sub_directories:
        children.append(build_tree(sub, validate))
    if len(children) == 2 and children[0] == -1:
        return None
    gov = Entity.get_org(root_dir)
    if children[0] == None:
        #leaf node 
        block = load_vote_block(root_dir)
    else:
        block = Block(children)
    block.load_id(root_dir + "/id")
    if validate:
        sig = block.sign_block(gov)
        if sig is None:
            print("error validating election")
            exit(5)
        block.save_sig(root_dir)
    else:
        block.load_sig(root_dir)
        if not block.verify_sig(gov):
            print("Election Is Invalid")
            exit(7)
    if root_dir.split("/")[-1:][0] in states:
        if validate:
            print("Validated: ", end="")
        else:
            print("Verified: ", end="")
        print(root_dir.split("/")[-1:][0])

    return block


def create_votes(states, candidates):

    with open("./election/names.json", "r") as f:
        names = json.load(f)
    
    path = Entity.data_path + "/us"
    us = Entity.get_org(path)
    us.save_entity(path)
    for state in states:
        state_gov = Entity.get_org(path + "/" + state)
        state_gov.get_id(us)
        state_gov.save_entity(path + "/" + state)
        for county in states[state]:
            county_dir = path + "/" + state + "/"+ county
            gov = Entity.get_org(county_dir)
            gov.get_id(state_gov)
            gov.save_entity(county_dir)
            used_names = set()
            for i in range(random.randint(1,10)):
                while True:
                    name = names[random.randint(0, len(names) - 1)]
                    if name not in used_names:
                        used_names.add(name)
                        break
                data = VoterData({"name":name, "county":county, "state":state})
                voter_path = county_dir + "/" + name + "/info"
                vote_path = county_dir + "/" + name + "/vote" 
                ind = Entity(voter_path + "/key.pub",voter_path + "/key.priv",data,None)
                #could also do it at the state level but doing this for simplicity
                ind.get_id(gov)
                ind.save_entity(voter_path)
                cand = candidates[random.randint(0, len(candidates) - 1)]
                vote = Vote.create_vote(VoteData(cand), ind)
                vote.save_vote(vote_path)
    
                



    

if __name__ == "__main__":
    main()
