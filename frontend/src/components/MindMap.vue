<template>
  <div id="mindMapContainer">
    <div class="menus">
        <div class="button-container">
          <span class="button">
            <v-btn prepend-icon="fas fa-arrow-right" @click="addChildNode" rounded="sm" style="margin-right: 10px; margin-top: 20px; margin-bottom: 10px;">
            </v-btn>
            <p>SonNode</p>
          </span>
          <span class="button">
            <v-btn prepend-icon="fas fa-bars" @click="addSameNode" rounded="sm" style="margin-right: 10px; margin-top: 20px; margin-bottom: 10px;">
            </v-btn>
            <p>SameNode</p>
          </span>
          <span class="button">
            <v-btn prepend-icon="fas fa-times" @click="removeNode" rounded="sm" style="margin-right: 10px; margin-top: 20px; margin-bottom: 10px;">
            </v-btn>
            <p>Remove</p>
          </span>
          <span class="button">
            <v-btn prepend-icon="fas fa-check-circle" @click="setToSupport" rounded="sm" style="margin-right: 10px; margin-top: 20px; margin-bottom: 10px;">
            </v-btn>
            <p>Support</p>
          </span>
          <span class="button">
            <v-btn prepend-icon="fas fa-exclamation-triangle" @click="setToObjection" rounded="sm" style="margin-right: 10px; margin-top: 20px; margin-bottom: 10px;">
            </v-btn>
            <p>Objection</p>
          </span>
          <span class="button">
            <v-btn prepend-icon="fas fa-database" @click="setToPremise" rounded="sm" style="margin-right: 10px; margin-top: 20px; margin-bottom: 10px;">
            </v-btn>
            <p>Premise</p>
          </span>
        </div>
</div>
  </div>
  <div class="context-me" v-if="showMenu" :style="{ top: menuY + 'px', left: menuX + 'px' }">
    <ul>
          <li @click="exploreClaims">
            <i class="fas fa-pen"></i> Explore claims
          </li>
          <li @click="brainstorm">
            <i class="fas fa-lightbulb"></i> Brainstorm
          </li>
          <li @click="addChildNode"><i class="fas fa-arrow-right"></i>Add child node</li>
          <li @click="addSameNode"><i class="fas fa-bars"></i>Add same node</li>
          <li @click="removeNode"><i class="fas fa-times"></i>Remove node</li>
          <li @click="setToSupport"><i class="fas fa-check-circle"></i>Set to support</li>
          <li @click="setToObjection"><i class="fas fa-exclamation-triangle"></i>Set to objection </li>
          <li @click="setToPremise"><i class="fas fa-database"></i>Set to premise </li>
    </ul>
  </div>
  <ChatModal
  :mindMapData="mindMapData"
  :visible="dialogVisible"
  @close="dialogVisible = false"
  :mode="mode"
  :claim="claim"
  :topic_id="topic_id"
  @reset-claim="resetClaim"
  >
  </ChatModal>
</template>

<script>
  import MindMap from "simple-mind-map"
  import axios from 'axios'
  import ChatModal from "@/components/ChatModal.vue";
  let mindMap = null;
  // 激活当前节点列表
  export default {
    name: 'MindMap',
    data() {
      return {
          topic_id: 4,
          activeNodes: [],
          showMenu: false,
          menuX: 0,
          menuY: 0,
          mode :null,
          dialogVisible:false,
          claim:'',
          mindMapData:null,
          clickContent:null,
      }
  },
    components:{
      ChatModal
    },
    mounted() {
    // eslint-disable-next-line
      mindMap = new MindMap({
          el: document.getElementById('mindMapContainer'),
          data: {
          "data": {
              "text": "根节点"
          },
          "children": []
        },
        initRootExpand: ['left', 'center']
      });
      mindMap.setTheme('simpleBlack')
      
      // 加载树结构
      this.loadTree(mindMap)
      
      mindMap.setThemeConfig({
        // lineColor: '#009CE0',
        lineWidth: 5,
      })
      
      mindMap.on('node_active', (node, nodeList) => {
        this.activeNodes = nodeList; // 使用 this 访问 activeNodes
        if(node){
          console.log(node)
          this.clickContent = node.nodeData.data.comment
          this.$emit('update-click-content', this.clickContent)
        }
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
          this.mode = 'Explore claims'
          this.claim = node.nodeData.data.text
        }else{
          this.mode = 'Brainstorm'
          this.claim = node.nodeData.data.text
        }
        if(!node.isRoot){
          this.showContextMenu(rect.cx,rect.cy + rect.h/2)
        }

    });
  },
    methods:{
      
      loadTree(mindMap){
        console.log("loadTree function is called");
        axios.get(`http://localhost:5000/tree/${this.topic_id}`)
        .then(response => {
          console.log(response.data)
          mindMap.setData({
            data: {
              text: response.data[0].data.text
            },
            children: response.data[0].children
          })
          this.mindMapData = mindMap.getData()
          console.log('this.mindMapData',this.mindMapData)
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
      this.mode = 'Brainstorm'
      this.showMenu = false
      this.dialogVisible = true; // 打开聊天窗口
    },
    exploreClaims(){
      this.mode = 'Explore claims'
      this.showMenu = false
      this.dialogVisible = true; // 打开聊天窗口
    },
    addChildNode() {
        // 确保至少有一个节点被激活
        if (this.activeNodes.length > 0) {
          // 获取当前激活的节点
          const activeNode = this.activeNodes[0];
          // 使用 mindMap.execCommand 添加子节点
          mindMap.execCommand('INSERT_CHILD_NODE', activeNode);
          this.showMenu = false; // 关闭上下文菜单
        }
      },
      addSameNode(){
        if (mindMap) {
          mindMap.execCommand('INSERT_NODE')
        }
        this.showMenu = false; // 关闭菜单
      },
      removeNode(){
        if (mindMap) {
          mindMap.execCommand('REMOVE_NODE')
        }
        this.showMenu = false; // 关闭菜单
      },
      setToSupport() {
        if (this.activeNodes.length > 0) {
          this.activeNodes.forEach(node => {
            node.setStyle('lineColor', '#008000')
            node.setStyle('lineStyle','curve')
            node.setStyle('lineWidth', 5)
            node.setStyle('fillColor', '#CCFFCC')
          })
          this.showMenu = false
        }
      },
      setToObjection() {
        if (this.activeNodes.length > 0) {
          this.activeNodes.forEach(node => {
            node.setStyle('lineColor', '#FF0000')
            node.setStyle('lineStyle','curve')
            node.setStyle('lineWidth', 5)
            node.setStyle('fillColor', '#FFCCCC')
          })
          this.showMenu = false
        }
      },
      resetClaim(){
        this.claim = ''
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
.menus{
border-radius: 10px;
box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
padding: 20px;
display: flex;
justify-content: center;
align-items: center;
/* 限制宽度 */
max-width: 500px; /* 例如设置最大宽度为 500px */
/* 自动换行 */
flex-wrap: wrap;
position:relative;
left:350px; 
top:10px;
}
/* .menus_button{
margin-right: 10px; 
margin-top: 20px; 
margin-bottom: 20px;
text-transform: capitalize;
} */

.button-container {
  display: flex; /* 使用 flex 布局 */
  flex-direction: row; /* 设置为横向排列 */
  align-items: center; /* 垂直居中 */
}
.button p{
  font-size: 12px;
  text-indent: -1em; /* 将文字缩进一个字符的宽度 */
}
</style>