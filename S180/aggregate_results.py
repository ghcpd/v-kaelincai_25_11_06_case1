import json
import os

def load(path):
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except Exception as e:
            return {'raw':open(path).read()}
    return None

pre = load('Project_A_PreFeature_Search/results/results_pre.json')
post = load('Project_B_PostFeature_Search/results/results_post.json')

report = {'pre':pre,'post':post}
print(json.dumps(report, indent=2))
