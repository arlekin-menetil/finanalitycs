<script setup>

defineProps({

  title: {
    type: String,
    default: "Ничего не найдено",
  },

  description: {
    type: String,
    default:
      "Попробуйте изменить фильтры или параметры поиска",
  },

  icon: {
    type: String,
    default: "🏦",
  },
})

</script>

<template>

<div class="empty">

  <!-- ===================================== -->
  <!-- 💣 ICON -->
  <!-- ===================================== -->
  <div class="icon">

    {{ icon }}

  </div>


  <!-- ===================================== -->
  <!-- 💣 TITLE -->
  <!-- ===================================== -->
  <h2>

    {{ title }}

  </h2>


  <!-- ===================================== -->
  <!-- 💣 DESCRIPTION -->
  <!-- ===================================== -->
  <p>

    {{ description }}

  </p>

</div>

</template>

<style scoped>

.empty{
display:flex;
flex-direction:column;
align-items:center;
justify-content:center;
text-align:center;
padding:90px 24px;
border-radius:30px;
background:white;
border:1px solid #e2e8f0;
box-shadow:
0 4px 20px rgba(0,0,0,.04);
}

.icon{
font-size:72px;
margin-bottom:24px;
line-height:1;
}

h2{
margin:0;
font-size:32px;
font-weight:900;
color:#0f172a;
}

p{
margin-top:14px;
max-width:520px;
font-size:16px;
line-height:1.7;
color:#64748b;
}

@media(max-width:768px){

.empty{
padding:70px 20px;
}

.icon{
font-size:56px;
}

h2{
font-size:26px;
}

p{
font-size:15px;
}

}

</style>