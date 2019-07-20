$(function() {


    //line
var ctxL = document.getElementById("lineChart").getContext('2d');
var myLineChart = new Chart(ctxL, {
  type: 'line',
  data: {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
        label: "Users",
        data: [55, 112, 198, 301, 374, 407, 489],
        backgroundColor: [
          'rgba(245,102,0, .2)',
        ],
        borderColor: [
          'rgba(245,102,0,0.8)',
        ],
        borderWidth: 2
      },
      {
        label: "Stores",
        data: [1, 5, 11, 18, 24, 44, 67],
        backgroundColor: [
          'rgba(0,208,93, .2)',
        ],
        borderColor: [
          'rgba(0,208,93,0.8)',
        ],
        borderWidth: 2
      },
      {
        label: "Sales",
        data: [122, 245, 442, 554, 675, 787, 889],
        backgroundColor: [
          'rgba(0,129,191, .2)',
        ],
        borderColor: [
          'rgba(0,129,191,0.8)',
        ],
        borderWidth: 2
      },
      
    ]
  },
  options: {
    responsive: true
  }
});
    
});

