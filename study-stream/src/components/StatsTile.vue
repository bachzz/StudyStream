<template>
  <div :class="statsIsOpen ? 'stats-wrapper open' : 'stats-wrapper'">
    <div>
      <button class="stats" @click="handleStatsClick">
        <template v-if="statsIsOpen">
          <img class="icon" :src="close" alt="" />
        </template>
        <template v-else>
          <img class="icon" :src="stats" alt="" />
        </template>
      </button>
    </div>

    <div class="stats-container">
      <div id="attention-chart">
        <apexchart ref="attentionChart" type="line" height="350" :options="attentionChartOptions" :series="attentionSeries"></apexchart>
      </div>

      <div id="EAR-chart">
        <apexchart ref="EARChart" type="line" height="350" :options="EARChartOptions" :series="EARSeries"></apexchart>
      </div>

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
      statsIsOpen: false,
      close,
      stats,

      attentionSeries: [{
          name: "attention score",
          data: [
            {
              x: 0,
              y: 0
            }
          ], 
      }],
      attentionChartOptions: {
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
          type: 'datetime',
          range: 120000, // ms
          labels: {
            format: 'HH:mm',
          }
        },
        yaxis: {
          min: 0,
          max: 1
        }
      },

      EARSeries: [{
          name: "EAR",
          data: [
            {
              x: 0,
              y: 0
            }
          ], 
      }],
      EARChartOptions: {
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
          text: 'Eye-Aspect-Ratio (EAR)',
          align: 'left'
        },
        grid: {
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        xaxis: {
          type: 'datetime',
          range: 120000, // ms
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
      var attentionData = [];
      var EARData = [];
      const statsUrl = "http://localhost:3000";
      var date = "";


      // update data series
      await axios({
        method: 'GET',
        url: statsUrl + "/data/",
      }).then(function(response) {
        // console.log(response);
        response.data.data.forEach(el => {
          var prob = el['prob'];
          var earVal = el['EAR_cur'];
          var time = el['time'].split(' ')[1];
          var hour = parseInt(time.split(':')[0]);
          var min = parseInt(time.split(':')[1]);
          var sec = parseInt(time.split(':')[2]);
          var time_ms = toMilliseconds(hour, min, sec);
          date = el['time'].split(' ')[0];

          attentionData.push({
            x: time_ms, 
            y: prob, 
          });

          EARData.push({
            x: time_ms, 
            y: earVal, 
          });
        });
      });


      me.$refs.attentionChart.updateSeries([{
        name: 'attention score',
        data: attentionData
      }]);

      me.$refs.attentionChart.updateOptions({
        title: {
          text: 'Attention Performance - ' + date
        },
      });

      me.$refs.EARChart.updateSeries([{
        name: 'EAR',
        data: EARData
      }]);

      me.$refs.EARChart.updateOptions({
        title: {
          text: 'Eye-Aspect-Ratio (EAR) - ' + date
        },
      });
    }, 3000)
  },

  methods: {
    handleStatsClick() {
      this.statsIsOpen = !this.statsIsOpen;
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


@media screen and (max-width: 700px) {
  .stats-container {
    width: calc(100% - 104px);
    right: calc((100% + 56px) * -1);
  }
}
</style>
