from common.dir_path import topic_summary_dir
from common.file_process import load_json
from common.cookies import generate_uid

class TreeServices:

    @staticmethod
    def get_claims_tree_structure(claims):
        children = []
        for claim in claims:
            content = claim['content']
            premises = claim['premises']
            attitude = claim.get('attitude', None)

            # 根据 attitude 设置颜色
            line_color = "#333333"  # 默认黑色
            if attitude == "objection":
                line_color = "#FF0000"  # 红色
            elif attitude == "support":
                line_color = "#008000"  # 绿色

            premises_children = [
                {'data': {'text': premise}, 'children': [], 'class': 'premise'} for premise in premises
            ]

            children.append(
                {
                    'data': {'text': content, 'lineColor': line_color},  # 添加 lineColor 属性
                    'children': premises_children
                }
            )
        return children


    @staticmethod
    def get_tree_structure(topic_id):
        print('processing tree structure')
        file = topic_summary_dir.joinpath(f'{topic_id}.json')
        data = load_json(file)

        tree_data = []

        for item in data:
            major_claim_content = item['major_claim']['content']
            claims = item['major_claim']['claims']

            claims_children = TreeServices.get_claims_tree_structure(claims)

            tree_data.append(
                {
                    'data': {'text': major_claim_content},
                    'children': claims_children
                }
            )

        return tree_data