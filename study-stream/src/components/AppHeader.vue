<template>
  <header>
    <div>
      <div class="row">
        <a class="right-border" target="_blank">
          <img class="header-icon" :src="studystream" alt="Study Stream" />
        </a>
        <p class="title">StudyStream</p>
      </div>
      <div class="row">
        <a
          href="https://github.com/bachzz/StudyStream"
          rel="noreferrer noopener"
          target="_blank"
        >
          <img class="header-icon" :src="github" alt="Github repo" />
        </a>
      </div>
    </div>
  </header>
</template>

<script>
import github from "../assets/github.svg";
import studystream from "../assets/header-logo.avif";
import newtab from "../assets/newtab.svg";

export default {
  name: "AppHeader",
  data() {
    return {
      github,
      // daily,
      studystream,
      newtab,
    };
  },
};
</script>

<style>
header {
  font-size: 12px;
  line-height: 16px;
  font-weight: bold;
  border-bottom: 1px solid #fff;
  padding: 2px;
  background-color: #fff;
}
header > div {
  max-width: 1200px;
  margin: auto;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.icon {
  height: 24px;
}

.header-icon {
  height: 50px;
}

.title {
  font-size: medium;
}

.row {
  display: flex;
  align-items: center;
}
/* .right-border {
  padding-right: 16px;
  border-right: 1px solid #c8d1dc;
  margin-right: 16px;
} */
.button-link {
  border: 1px solid #c8d1dc;
  border-radius: 8px;
  padding: 7px 16px;
}
@media screen and (max-width: 700px) {
  .button-link {
    display: none;
  }
}
</style>
