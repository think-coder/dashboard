<template>
  <el-container direction="vertical" style="height: 500px; border: 1px solid #eee">
    <el-header>
      <el-menu 
      default-active="1" 
      class="el-menu-demo" 
      mode="horizontal" 
      background-color="#B3C0D1"
      text-color="#333"
      active-text-color="blue">
        <el-menu-item index="1" name="1">处理中心-1</el-menu-item>
        <el-menu-item index="2" name="2">处理中心-2</el-menu-item>
        <el-menu-item index="3" name="3">处理中心-3</el-menu-item>
        <el-menu-item index="4" name="4">处理中心-4</el-menu-item>
      </el-menu>
    </el-header>
    <el-container direction="horizontal">
      <el-aside width="200px">Aside</el-aside>
      <el-container direction="vertical">
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<style>
  .el-header, .el-footer{
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
</style>
