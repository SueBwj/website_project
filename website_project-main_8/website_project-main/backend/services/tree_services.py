from common.dir_path import topic_summary_dir
from common.file_process import load_json
from common.cookies import generate_uid

class TreeServices:

    @staticmethod
    def get_subcomments_tree_structure(subcomments):
        sub_children = []
        for subcomment in subcomments:
            sub_claim = subcomment['claim']
            if sub_claim is None or sub_claim == '':
                continue
            sub_comment = subcomment['comment']
            if sub_comment is None or sub_comment == '':
                continue
            sub_evidences = subcomment['evidence']
            sub_objections = subcomment['objections']
            nested_subcomments = subcomment.get('subcomments', [])

            subcomment_children = [
                {'data':{'text':sub_comment},'children':[], 'class':'comment'}
            ]

            subevidences_children = [
                {'data':{'text':evidence}, 'children':[], 'class':'evidence'} for evidence in sub_evidences
            ]

            sub_objections_children = [
                {'data':{'text':objection['content'], 'class':'objectionContent'},
                  'children':[{'data':{'text':objection['response'], 'class':'objectionResponse'}, 'children':[]}]}  for objection in sub_objections
            ]

            sub_children.append(
                    {
                    'data':{'text':"Claim"},
                    'children': [{
                        'data':{'text':sub_claim}, 
                        'children':[
                            {'data':{'text':"Comment", 'class':'commentClass'},'children':subcomment_children},
                            {'data':{'text':'Evidence', 'class':'evidenceClass'},'children':subevidences_children},
                            {'data':{'text':'Objections', 'class':'objectionClass'},'children':sub_objections_children}
                            ]
                        }]
                    }
                )
            
            if nested_subcomments:
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
            if claim is None or claim == '':
                continue
            # comment 就是一个字符串
            comment = item['comment']
            if comment is None or comment == '':
                continue
            evidences = item['evidence']
            objections = item['objections']
            subcomments = item['subcomments']
            sub_children = TreeServices.get_subcomments_tree_structure(subcomments)

            comment_children = [
                {'data':{'text':comment},'children':sub_children, 'class':'comment'}
            ]

            evidences_children = [
                {'data':{'text':evidence}, 'children':[], 'class':'evidence'} for evidence in evidences
            ]

            objections_children = [
                {'data':{'text':objection['content'], 'class':'objectionContent'}, 
                 'children':[{'data':{'text':objection['response'], 'class':'objectionResponse'}, 'children':[]}]}  for objection in objections
            ]
            children.append(
                {'data':{'text':claim},
                 'children':[
                    {'data':{'text':"Comment"},'children':comment_children, 'class':'commentClass'},
                    {'data':{'text':'Evidence'},'children':evidences_children, 'class':'evidenceClass'},
                    {'data':{'text':'Objections'},'children':objections_children, 'class':'objectionClass'}
                    ]
                 }
                )

        return children


        