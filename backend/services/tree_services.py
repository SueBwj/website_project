from common.dir_path import topic_summary_dir
from common.file_process import load_json

class TreeServices:

    @staticmethod
    def get_subcomments_tree_structure(subcomments):
        print('processing subcomments tree structure')
        sub_children = []
        for subcomment in subcomments:
            sub_claim = subcomment['claim']
            sub_comments = subcomment['comment']
            sub_evidences = subcomment['evidence']
            sub_objections = subcomment['objections']
            nested_subcomments = subcomment.get('subcomments', [])

            subcomment_children = [
                {'data':{'text':sub_comment},'children':[] } for sub_comment in sub_comments
            ]

            subevidences_children = [
                {'data':{'text':evidence}, 'children':[]} for evidence in sub_evidences
            ]

            sub_objections_children = [
                {'data':{'text':objection['content']}, 'children':[{'data':{'text':objection['response']}, 'children':[]}]}  for objection in sub_objections
            ]

            sub_children.append(
                {'data':{'text':sub_claim},
                 'children':[
                    {'data':{'text':"Comment"},'children':subcomment_children},
                    {'data':{'text':'Evidence'},'children':subevidences_children},
                    {'data':{'text':'Objections'},'children':sub_objections_children}
                    ]
                 }
                )
            
            if nested_subcomments:
                print('processing nested subcomments tree structure')
                sub_children.extend(TreeServices.get_subcomments_tree_structure(nested_subcomments))


        return sub_children

    @staticmethod
    def get_tree_structure(topic_id):
        print('processing tree structure')
        file = topic_summary_dir.joinpath(f'{topic_id}.json')
        data = load_json(file)
        
        children = []

        for item in data:
            claim = item['claim']
            # comment 就是一个字符串
            comments = item['comment']
            evidences = item['evidence']
            objections = item['objections']
            subcomments = item['subcomments']
            sub_children = TreeServices.get_subcomments_tree_structure(subcomments)

            comment_children = [
                {'data':{'text':comment},'children':sub_children} for comment in comments
            ]

            evidences_children = [
                {'data':{'text':evidence}, 'children':[]} for evidence in evidences
            ]

            objections_children = [
                {'data':{'text':objection['content']}, 'children':[{'data':{'text':objection['response']}, 'children':[]}]}  for objection in objections
            ]
            children.append(
                {'data':{'text':claim},
                 'children':[
                    {'data':{'text':"Comment"},'children':comment_children},
                    {'data':{'text':'Evidence'},'children':evidences_children},
                    {'data':{'text':'Objections'},'children':objections_children}
                    ]
                 }
                )

        return children


        