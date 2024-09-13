<template>
    <div id="mindMapContainer"></div>
</template>
  
<script>
    import MindMap from "simple-mind-map"
    import axios from 'axios'

    export default {
    data() {
        return {
            topic_id: 1
        }
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
        }
      });
      this.loadTree(mindMap); // 等待 loadTree 完成
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
</style>