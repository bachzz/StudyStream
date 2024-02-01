<template>
  <div :class="chatIsOpen ? 'stats-wrapper open' : 'stats-wrapper'">
    <div>
      <button class="stats" @click="handleChatClick">
        <template v-if="chatIsOpen">
          <img class="icon" :src="close" alt="" />
        </template>
        <template v-else>
          <img class="icon" :src="stats" alt="" />
        </template>
      </button>
    </div>

    <div class="stats-container">
      <div id="chart">
        <apexchart ref="chart" type="line" height="350" :options="chartOptions" :series="series"></apexchart>
      </div>

      <button @click="test">test</button>

    </div>
  </div>
</template>

<script>
import close from "../assets/x.svg";
import stats from "../assets/statistics.svg";
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  name: "ChatTile",
  components: {
    apexchart: VueApexCharts,
  },
  props: ["sendMessage", "messages"],
  data() {
    return {
      // last_x : 0,
      // last_y : 0,
      chatIsOpen: false,
      close,
      stats,
      // statsUrl: 'http://localhost:3000',

      series: [{
          name: "attention score",
          data: [
            {
              x: 0,
              y: 0
            }
          ], 
          // [0.05 , 0.205, 0.175, 0.255, 0.245, 0.31 , 0.345, 0.455, 0.74 ], //[10, 41, 35, 51, 49, 62, 69, 91, 148]
      }],
      chartOptions: {
        chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          },
          animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
              speed: 1000
            }
          },
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        title: {
          text: 'Attention Performance',
          align: 'left'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        xaxis: {
          // categories: [], 
          //['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
          type: 'datetime',
          range: 120000, //777600000, //5,
          labels: {
            format: 'HH:mm',
          }
        },
        yaxis: {
          min: 0,
          max: 1
        }
      },
    };
  },

  mounted: function () {
    var me = this;
    const toMilliseconds = (hrs,min,sec) => (hrs*60*60+min*60+sec)*1000;
    var count = 0;

    window.setInterval(async function () {
      var data = [];
      const statsUrl = "http://localhost:3000";
      // var x = [];
      // var y = [];
      var timestamps = []; 
      var date = "";
      // var rand = (Math.random() * (1.00 - 0.00)).toFixed(2);

      // if (isNaN(this.last_x)){this.last_x = 0}
      // if (isNaN(this.last_y)){this.last_y = 0}

      // if (count < 10){
      //   this.last_x = this.last_x+500; //86400000;
      //   this.last_y = rand; //this.last_y+rand;
      //   // console.log(this.last_x);
      //   // console.log(this.last_y);
      // }
      // var last_x = this.last_x;
      // var last_y = this.last_y;
      // count = count+1;

      // update data series
      await axios({
        method: 'GET',
        url: statsUrl + "/data/",
      }).then(function(response) {
        
        response.data.forEach(el => {
          var prob = el['prob'];
          var time = el['time'].split(' ')[1];
          var hour = parseInt(time.split(':')[0]);
          var min = parseInt(time.split(':')[1]);
          var sec = parseInt(time.split(':')[2]);
          var time_ms = toMilliseconds(hour, min, sec);
          date = el['time'].split(' ')[0];

          data.push({
            x: time_ms, //last_x, //parseInt(el['id']),
            y: prob, //el['prob']
          });
        });
      });

      // console.log(data);
      // // update categories
      // await axios({
      //   method: 'GET',
      //   url: statsUrl + "/time/",
      // }).then(function(response) {
        
      //   response.data.forEach(el => {
      //     timestamps.push(el['time'].split(" ")[1]);
      //     // data.push(parseInt(el['id']) );
      //   });

      //   date = response.data[0]['time'].split(" ")[0];

      // });

      me.$refs.chart.updateSeries([{
        name: 'attention score',
        data: data
      }]);

      me.$refs.chart.updateOptions({
        title: {
          text: 'Attention Performance - ' + date
        },
        // xaxis: {
        //   // categories: timestamps,
        //   range: 5,
        // }
      });
    }, 3000)
  },

  methods: {
    async test(){
      var probs = [];
      var timestamps = []; 
      var date = "";

      // update probs series
      await axios({
        method: 'GET',
        url: this.statsUrl + "/data/",
      }).then(function(response) {
        
        response.data.forEach(el => {
          probs.push(el['prob']);
        });
      });

      this.$refs.chart.updateSeries([{
        name: 'attention score',
        data: probs
      }]);

      // update probs series
      await axios({
        method: 'GET',
        url: this.statsUrl + "/time/",
      }).then(function(response) {
        
        response.data.forEach(el => {
          timestamps.push(el['time'].split(" ")[1]);
        });

        date = response.data[0]['time'].split(" ")[0];

      });

      this.$refs.chart.updateOptions({
        title: {
          text: 'Attention Performance - ' + date
        },
        xaxis: {
          categories: timestamps
        }
      });


      
    },

    // Toggle chat's view (open/closed)
    handleChatClick() {
      this.chatIsOpen = !this.chatIsOpen;
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
  width: 548px;
  height: 100%;
  transition: right 0.5s ease-out;
  right: -555px;
  display: flex;
  align-items: center;
}
.stats-wrapper.open {
  right: 0;
}
.stats-container {
  background-color: #fff;
  width: 500px;
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
  right: 548px;
}
.messages {
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

.chat-message {
  color: #121a24;
  text-align: left;
  font-size: 14px;
  line-height: 18px;
  margin: 0 0 20px;
}
.chat-message .chat-name {
  color: #6b7785;
}

@media screen and (max-width: 700px) {
  .stats-container {
    width: calc(100% - 104px);
    right: calc((100% + 56px) * -1);
  }
}
</style>
