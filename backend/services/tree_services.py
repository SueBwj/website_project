from common.dir_path import topic_summary_dir
from common.file_process import load_json
from common.cookies import generate_uid

class TreeServices:

    @staticmethod
    def get_comment_tree_structure(comment, depth=0):
        """递归地构建评论树结构."""
        content = comment.get('comment', '')  # 获取评论内容，如果没有则为空字符串
        name = comment.get('name', 'Anonymous') # 获取用户名，如果没有则为Anonymous

        major_claim = comment.get('major_claim', {}) # 获取major_claim,如果不存在则返回空字典
        if not major_claim:
            return {'data': {}, 'children': []}
        major_claim_content = major_claim.get('content', "[Content Missing]")

        claims = comment['major_claim']['claims']
        attitude = comment.get('attitude', 'support')
        
        # 根据 attitude 设置颜色
        # line_color = "#008000"  #默认绿色
        fill_color = "#CCFFCC"
        if attitude == "objection":
            # line_color = "#FF0000"
            fill_color = "#FFCCCC"  # 红色
        elif attitude == "support": 
            # line_color = "#008000"
            fill_color = "#CCFFCC"  # 绿色


        claims_children = TreeServices.get_claims_tree_structure(claims, depth)

        children = claims_children + [ # 添加claims children
            TreeServices.get_comment_tree_structure(subcomment, depth+1) for subcomment in comment.get('subcomments', [])
        ]
        # 为每个节点添加 name 属性
        node_data = {'text': f"{name}: {major_claim_content}", 'comment': content, 'fillColor': fill_color}
        if depth >= 2:
            node_data['expand'] = False
        
        return {'data': node_data, 'children': children}
    

    @staticmethod
    def get_claims_tree_structure(claims, depth):
        """构建论据的树结构."""
        children = []
        for claim in claims:
            content = claim['content']
            premises = claim['premises']
            attitude = claim.get('attitude', 'support')

            # 根据 attitude 设置颜色
            # line_color = "#008000"  

            fill_color = "#CCFFCC" # 填充颜色
            premises_fill_color = "#A1CAFF"

            premises_children = [
                {'data': {'text': premise,  'fillColor': premises_fill_color}, 'expand': depth >= 2, 'children': [], 'class': 'premise'} for premise in premises
            ]
            
            children.append(
                {
                    'data': {'text': content, 'fillColor': fill_color},  # 添加 lineColor 属性
                    'children': premises_children
                }
            )
        return children


    @staticmethod
    def get_tree_structure(topic_id):
        """构建整个主题的树结构."""
        file = topic_summary_dir.joinpath(f'{topic_id}.json')
        data = load_json(file)

        tree_data = []

        for item in data:
            tree_data.append(TreeServices.get_comment_tree_structure(item, depth=0))

        return tree_data