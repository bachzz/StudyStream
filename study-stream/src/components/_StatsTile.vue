<template>
    <div :class="statsIsOpen ? 'stats-wrapper open' : 'stats-wrapper'">
      <div>
        <button class="stats" @click="handleStatsClick">
          <template v-if="statsIsOpen">
            <img class="icon" :src="close" alt="" />
          </template>
          <template v-else>
            <img class="icon" :src="chat" alt="" />
          </template>
        </button>
      </div>
    </div>

    <div class="stats-container">
      <div class="stats-messages">
        <p
          v-for="({ name = '', message = '' }, i) in messages"
          :key="i"
          class="stats-message"
        >
          <span class="stats-name">{{ name }}: </span>{{ message }}
        </p>
      </div>

      <form @submit="submitForm">
        <div class="input">
          <label for="message">Type a message...</label>
          <textarea
            id="message"
            v-model="text"
            type="text"
            placeholder="Type a message..."
            @keydown.enter="submitForm"
          />
        </div>

        <button class="stats-submit-button" type="submit">
          <img :src="send" alt="" />
        </button>
      </form>
    </div>

</template>


<script>
import close from "../assets/x.svg";
import chat from "../assets/chat.svg";
import send from "../assets/send.svg";

export default {
  name: "StatsTile",
  props: ["sendMessage", "messages"],
  data() {
    return {
      statsIsOpen: false,
      close,
      chat,
      send,
      text: "",
    };
  },
  methods: {
    // Toggle chat's view (open/closed)
    handleStatsClick() {
      this.statsIsOpen = !this.statsIsOpen;
    },
    // Send chat message using prop method from CallTile.vue
    submitForm(e) {
      e.preventDefault();

      this.sendMessage(this.text);
      this.text = "";
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Ropa+Sans&display=swap");

.stats-wrapper {
  position: absolute;
  right: 0;
  top: 0;
  width: 348px;
  height: 100%;
  transition: right 0.5s ease-out;
  right: -300px;
  display: flex;
  align-items: center;
}
.stats-wrapper.open {
  right: 0;
}
.stats-container {
  background-color: #fff;
  width: 0px;
  display: flex;
  flex-direction: column;
  padding: 24px;
  height: calc(100% - 48px);
}
button.stats {
  background-color: #fff;
  border: none;
  cursor: pointer;
  border-radius: 16px 0 0 16px;
  padding: 16px 14px 13px 18px;
  position: absolute;
  top: calc(50% - 150px);
  right: 348px;
}
.stats-messages {
  flex: 1;
  padding-right: 32px;
}
.input {
  display: flex;
  flex-direction: column;
  flex: 1;
  align-items: flex-start;
}
label {
  color: #fff;
}
.input textarea {
  width: 100%;
  border: none;
  resize: none;
  font-family: "Ropa Sans", sans-serif;
  font-size: 16px;
}
.input textarea::placeholder {
  font-family: "Ropa Sans", sans-serif;
  font-size: 16px;
}
form {
  display: flex;
  border-bottom: 2px solid #c8d1dc;
}

.submit-button {
  padding: 4px;
  margin: 0 0 0 16px;
  border: none;
  background-color: #fff;
}

.stats-message {
  color: #121a24;
  text-align: left;
  font-size: 14px;
  line-height: 18px;
  margin: 0 0 20px;
}
.stats-message .stats-name {
  color: #6b7785;
}

@media screen and (max-width: 700px) {
  .stats-container {
    width: calc(100% - 104px);
    right: calc((100% + 56px) * -1);
  }
}
</style>