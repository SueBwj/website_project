<template>
  <div class="topic">
    <h4>Topic</h4>
    <v-card  
        class="mx-auto"
        variant="text"
      >
      <div>
      <v-card-item>
        <template v-slot:prepend>
          <v-avatar
            color="grey-darken-3"
            image="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-avatar>
        </template>
        <v-card-title class="text-left">Nicole</v-card-title>
        <v-card-subtitle class="text-left">Vue Creator</v-card-subtitle>
      </v-card-item>
      <h2 class="text-left pl-4 font-weight-bold" :style="{ fontSize: '20px' }">rights from people who engage with anti-Zionism and Gaza as atrendy cause</h2>
      <v-card-text class="py-1 text-left pl-10" :style="{ fontSize: '15px' }">
        {{ comments[0].comment }}
      </v-card-text>
    </div>
      
    </v-card>
  </div>
  <div class="comments pt-5">
    <h3 >Comments</h3>
    <div class="row m-2">
      <CardVuetify
       v-for="(comment,index) in comments[0].subcomment" 
       :comments="comment" 
       :key="index"
       :clickContent="clickContent"
       :replyComment="replyComment"
       />
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import CardVuetify from './CardVuetify.vue'
import jsonComment from '../../../backend/files/comment_data/discussion_subset1.json'
export default {
name: 'CommentReddit',
components: {
  CardVuetify
},
props: {
  clickContent: {
    type: String,
    default: ''
  },
  replyComment: {
    type: String,
    default: ''
  }
},
data(){
  return {
    comments:jsonComment,
  }
},
watch: {
  clickContent(newVal) {
    console.log("clickContent", newVal)
  },
  replyComment(newVal) {
    console.log("replyComment", newVal)
  }
},
}

</script>
<style>

</style>