from common.dir_path import topic_summary_dir
from common.file_process import load_json

class TreeServices:

    def get_tree_structure(topic_id):
        file = topic_summary_dir.joinpath(f'{topic_id}.json')
        data = load_json(file)
        
        children = []

        for item in data:
            claim = item['claim']
            comments = item['comments']
            children.append({'data':{'text':claim},'children':[{'data':{'text':el['comment']}, 'children':[]} for el in comments]})

        return children


        