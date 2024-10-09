<template>
  <div class="comment">
    <v-card  
        class="mx-auto pl-1"
        :class="{'highlight-card': isActive}"
        ref="cardRef"
        variant="text"
      >
      <div class="border-s-lg">
      <v-card-item>
        <template v-slot:prepend>
          <v-avatar
            color="grey-darken-3"
            image="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-avatar>
        </template>
        <v-card-title class="text-left">{{ comments.name }}</v-card-title>
        <v-card-subtitle class="text-left">Vue Creator</v-card-subtitle>
      </v-card-item>
      <v-card-text class="py-1 text-left" >
         {{ comments.comment }}
      </v-card-text>
    </div>
      <v-card-actions class="custom-actions">
         <!-- 修改的部分开始 -->
         <div class="support-container">
          <div class="circle" @click="handleClick" :class="isUp ? 'check' : ''">
            <div class="img-box" :class="isUp ? 'img-box-check' : ''">
              <img v-if="isUp" src="../assets/heart.svg" alt="" />
              <img v-else src="../assets/heart-outline.svg" alt="" />
            </div>
          </div>
          <div class="support-num">{{ support }}</div>
        </div>
        <!-- 修改的部分结束 -->
        <v-spacer></v-spacer>

        <v-btn
          v-if="comments.subcomment.length > 0"
          :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          @click="show = !show"
          color="black"
          :style="{
          fontSize: '15px',
          textTransform: 'capitalize',
          padding: '2px 6px',          /* 减小 padding 使按钮更细长 */
          borderRadius: '4px',        /* 设置较小的圆角或为 0 */
          height: '30px',             /* 可选：设置固定高度 */
          minWidth: '60px'            /* 可选：设置最小宽度 */
        }"
        >Reply</v-btn>
      </v-card-actions>

      <v-expand-transition>
        <div v-show="show">
          <card-vuetify :comments = "item"  v-for="(item,index) in comments.subcomment" :key="index" ref="childCards" />
        </div>
      </v-expand-transition>
    </v-card>
  </div>
  </template>
  <script>
  export default {
    name:"CardVuetify",
    props:{
        comments:{
            type: Object,
            default: () => {
                return {}
            }
        },
        clickContent: {
          type: String,
          default: ''
        },
        replyComment: {
          type: String,
          default: ''
        }
    },
    data: () => ({
      show:false,
      isUp: false,
      support:0,
      isActive: false
    }),
    methods: {
    handleClick () {
      if(this.isUp==false)
        this.support=this.support+1
      else
        this.support=this.support-1
      this.isUp = !this.isUp
    },
    scrollToCard() {
      this.$refs.cardRef.$el.scrollIntoView({ behavior: 'smooth' });
    },
    highlightAndScroll() {
      this.isActive = true;
      this.$nextTick(() => {
        this.scrollToCard();
      });
    },
    checkContent(content, compare_content) {
      return content && compare_content && content.toLowerCase().includes(compare_content.toLowerCase());
    },
    handleClickContentChange() {
      this.recursivelyCheckContent(this, this.clickContent);
    },
    handleReplyCommentChange() {
      this.recursivelyCheckContent(this, this.replyComment);
    },
    recursivelyCheckContent(component, compare_content) {
      // 检查当前组件的评论
      if (this.checkContent(component.comments.comment, compare_content)) {
        component.highlightAndScroll();
      return true; // 找到匹配项，返回true
    }

    // 展开子评论
    component.show = true;

    // 检查子评论
    if (component.comments.subcomment && component.comments.subcomment.length > 0) {
      this.$nextTick(() => {
        const childCards = component.$refs.childCards;
        if (Array.isArray(childCards)) {
          for (let childCard of childCards) {
            if (this.recursivelyCheckContent(childCard, compare_content )) {
              return true; // 如果在子组件中找到匹配项，返回true
            }
          }
        } else if (childCards) {
          // 只有一个子组件的情况
          if (this.recursivelyCheckContent(childCards, compare_content)) {
            return true;
          }
        }
      });
    }

      // 如果没有找到匹配项
      component.isActive = false;
      return false;
    },
  },
  watch: {
      clickContent: {
        handler: 'handleClickContentChange',
      },
      replyComment: {
        handler: 'handleReplyCommentChange',
      }
    }
}
</script>
<style>

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

.comment {
  margin: 0.5em 0; /* 减小上下间距 */
  padding: 0.8em; /* 减小内边距 */
  border-radius: 12px; /* 增加圆角 */
  height: auto; 
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 柔和的阴影 */
  transition: all 0.3s ease; /* 添加过渡效果 */
  position: relative;
  z-index: 1;
}

.highlight-card {
  border: 3px solid #ff4081;
  box-shadow: 0 0 15px rgba(255, 64, 129, 0.5);
  background-color: #fff9c4;
  transform: scale(1.02);
  transition: all 0.3s ease;
  z-index: 2;
}

.highlight-card:hover {
  box-shadow: 0 0 20px rgba(255, 64, 129, 0.7);
}

.comment:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 悬停时增加阴影 */
}

.v-card {
  max-width: 100%; /* 限制最大宽度 */
  margin: 0 auto; /* 居中显示 */
  overflow: visible;
}

.v-card-title {
  font-size: 1em; /* 稍微减小标题大小 */
  font-weight: 500; /* 稍微加粗 */
}

.v-card-subtitle {
  font-size: 0.8em; /* 稍微减小副标题大小 */
  color: #666; /* 更柔和的颜色 */
}

.v-card-text {
  font-size: 0.6em; /* 稍微减小正文大小 */
  line-height: 1.5; /* 增加行高 */
}

/* 调整点赞和回复按钮样式 */
.v-btn {
  font-size: 0.9em;
  text-transform: none; /* 取消全大写 */
  min-width: 64px; /* 减小最小宽度 */
}

/* 调整头像大小 */
.v-avatar {
  width: 40px;
  height: 40px;
}
.circle {
  position: relative;
  left: 20px;
  bottom: -25px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0px 0px 0px 0px rgba(223, 46, 58, 0.5);
  display: flex; /* 添加 Flexbox */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}


.img-box {
  width: 30px;
  height: 30px;
  user-select: none; /* 防止选中图片 */
  display: flex; /* 使用 Flexbox */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}

.img-box img {
  width: 20px; /* 根据需要调整 */
  height: 20px; /* 根据需要调整 */
}

.check {
  transition: box-shadow 0.5s;
  box-shadow: 0px 0px 0px 1em rgba(226, 32, 44, 0);
}

.img-box-check {
  animation: anm 0.5s;
}


/* 移除嵌套评论的左边距 */
.v-expand-transition .comment {
  margin-left: 0;
}
/* 确保展开的内容不会重叠 */
.v-expand-transition {
  overflow: visible;
}

@keyframes anm {
  0% {
    transform: scale(0);
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
  }
  50% {
    transform: scale(1.3);
    -webkit-transform: scale(1.3);
    -moz-transform: scale(1.3);
  }
  100% {
    transform: scale(1);
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
  }
}

/* 以下为处理兼容代码，可不看。*/

@-moz-keyframes anm {
  0% {
    transform: scale(0);
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
  }
  50% {
    transform: scale(1.3);
    -webkit-transform: scale(1.3);
    -moz-transform: scale(1.3);
  }
  100% {
    transform: scale(1);
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
  }
}

@-webkit-keyframes anm {
  0% {
    transform: scale(0);
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
  }
  50% {
    transform: scale(1.3);
    -webkit-transform: scale(1.3);
    -moz-transform: scale(1.3);
  }
  100% {
    transform: scale(1);
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
  }
}

@-o-keyframes anm {
  0% {
    transform: scale(0);
    -webkit-transform: scale(0);
    -moz-transform: scale(0);
  }
  50% {
    transform: scale(1.3);
    -webkit-transform: scale(1.3);
    -moz-transform: scale(1.3);
  }
  100% {
    transform: scale(1);
    -webkit-transform: scale(1);
    -moz-transform: scale(1);
  }
}
.support-num{
  position: relative;
  left: 45px;
  font-size: 15px;
}
</style>