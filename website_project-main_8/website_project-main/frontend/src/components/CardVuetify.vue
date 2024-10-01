<template>
  <div class="comment">
    <v-card  
        class="mx-auto pl-1"
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
        <v-card-title class="text-left">{{ comments.author }}</v-card-title>
        <v-card-subtitle class="text-left">Vue Creator</v-card-subtitle>
      </v-card-item>
      <v-card-text class="py-1 text-left" :style="{ fontSize: '20px' }">
         {{ comments.content }}
      </v-card-text>
    </div>
      <v-card-actions>
        <div>
          <div class="circle flex-h" @click="handleClick" :class="isUp?'check':''">
            <div class="img-box" :class="isUp?'img-box-check':''">
              <img v-if="isUp" src="../assets/heart.svg" alt="" />
              <img v-else src="../assets/heart-outline.svg" alt="" />
            </div>
          </div>
          <div class="support-num">{{this.support}}</div>
        </div>
        <v-spacer></v-spacer>

        <v-btn
          v-if="comments.replies.length > 0"
          :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
          @click="show = !show"
          color="black"
           :style="{ fontSize: '15px', textTransform: 'capitalize' }"
        >Reply</v-btn>
      </v-card-actions>

      <v-expand-transition>
        <div v-show="show">
          <card-vuetify :comments = "item"  v-for="(item,index) in comments.replies" :key="index"/>
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
        }
    },
    data: () => ({
      show:false,
      isUp: false,
      support:0
    }),
    methods: {
    handleClick () {
      if(this.isUp==false)
        this.support=this.support+1
      else
        this.support=this.support-1
      this.isUp = !this.isUp
    }
  }
  }
</script>
<style>
.comment {
  margin-left: 2em;
}
.circle {
  position:relative;
  left: 20px;
  bottom: -28px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0px 0px 0px 0px rgba(223, 46, 58, 0.5)
}
.img-box {
  position: absolute;
  left: 50%;
  top: 50%;
  margin-left: -25px;
  margin-top: -25px;
  width: 30px;
  height: 30px;
  /*margin: 5px;*/
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  -khtml-user-select: none;
  user-select: none; /* 防止快速点击图片被选中，可不加，为提高体验，博主加上了这几行代码。*/
}

.check {
  -webkit-transition: box-shadow 0.5s;
  -moz-transition: box-shadow 0.5s;
  -o-transition: box-shadow 0.5s;
  transition: box-shadow 0.5s;
  box-shadow: 0px 0px 0px 1em rgba(226, 32, 44, 0);
}
.img-box-check {
  animation: anm 0.5s;
  -moz-animation: anm 0.5s;
  -webkit-animation: anm 0.5s;
  -o-animation: anm 0.5s;
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
  bottom: 25px;
  font-size: 25px;
}
</style>