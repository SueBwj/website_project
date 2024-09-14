<template>
    <div id="mindMapContainer"></div>
    <div class="context-me" v-if="showMenu" :style="{ top: menuY + 'px', left: menuX + 'px' }">
      <ul>
            <li @click="addNote">
              <i class="fas fa-pen"></i> 备注
            </li>
            <li @click="brainstorm">
              <i class="fas fa-lightbulb"></i> {{ this.mode }}
            </li>
        </ul>
    </div>
    <ChatModal
    :visible="dialogVisible"
    @close="dialogVisible = false"
    :mode="mode"
    >
    </ChatModal>
</template>
  
<script>
    import MindMap from "simple-mind-map"
    import axios from 'axios'
    import ChatModal from "@/components/ChatModal.vue";


    export default {
    data() {
        return {
            topic_id: 1,
            activeNodes: [],
            showMenu: false,
            menuX: 0,
            menuY: 0,
            mode : null,
            dialogVisible:false
        }
    },
    components:{
      ChatModal
    },
    mounted() {
      
      // eslint-disable-next-line
      const mindMap = new MindMap({
          el: document.getElementById('mindMapContainer'),
          data: {
          "data": {
              "text": "根节点"
          },
          "children": []
        },
        initRootNodePosition: ['left', 'center']
      });
      this.loadTree(mindMap); // 等待 loadTree 完成

      mindMap.on('node_active', (node, nodeList) => {
        this.activeNodes = nodeList; // 使用 this 访问 activeNodes
        if(!node){
          this.showMenu = false
        }
      });
      mindMap.on('node_contextmenu',(event, node) => {
        console.log('click node and event information: ', node)
        console.log('click right')
        const rect = node.getRect()
        const is_comment = node.children.length === 0 ? true : false
        if(!is_comment){
          this.mode = '角色扮演'
        }else{
          this.mode = '头脑风暴'
        }
        if(!node.isRoot){
          this.showContextMenu(rect.cx,rect.cy + rect.h/2)
        }
        
      })
    },
    methods:{
      loadTree(mindMap){
        axios.get(`http://localhost:5000/tree/${this.topic_id}`)
          .then(response => {
            mindMap.setData({
              data:{
                'text': '萝卜快跑'
              },
              children : response.data
            })
          })
          .catch(error => {
            console.error("Error loading tree data:", error)
          })
      },
      showContextMenu(x,y) {
        this.showMenu = true;
        this.menuX = x; // 获取鼠标点击位置
        this.menuY = y;
        console.log("x坐标是",this.menuX)
        console.log("y坐标是",this.menuY)
        console.log('menu')
      },
      brainstorm(){
        this.showMenu = false
        this.dialogVisible = true; // 打开聊天窗口
      },
      addNote(){
        this.showMenu = false
      }
    }
}
</script>
  
<style>
  
  #mindMapContainer {
    width: 100%;
    height: 800px;
  }

  #mindMapContainer * {
    margin: 0;
    padding: 0;
  }

  .context-me {
    position: absolute;
    z-index: 1000;
    width: 180px;
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}

.context-me ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.context-me ul li {
    padding: 12px 16px;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
    color: #333;
    display: flex;
    align-items: center;
}

.context-me ul li:hover {
    background-color: #f0f0f0;
}

.context-me ul li i {
    margin-right: 10px;
    color: #555;
    transition: color 0.2s;
}

.context-me ul li:hover i {
    color: #007bff;
}

</style>