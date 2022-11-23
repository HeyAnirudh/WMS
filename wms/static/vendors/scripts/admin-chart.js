var ctx = document.getElementById("myChart").getContext("2d");

var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sept",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "User 1", // Name the series
        data: [
          4000, 5040, 2424, 14040, 8141, 5111, 3544, 4700, 6555, 7811, 9763,
          2093,
        ], // Specify the data values array
        fill: false,
        borderColor: "#2196f3", // Add custom color border (Line)
        backgroundColor: "#2196f3", // Add custom color background (Points and Fill)
        borderWidth: 1, // Specify bar border width
        tension: 0.5,
      },
      {
        label: "User 2", // Name the series
        data: [
          10880, 8942, 4545, 7588, 9900, 2482, 7417, 5504, 5900, 4570, 8753,
          2380,
        ], // Specify the data values array
        fill: false,
        borderColor: "#4CAF50", // Add custom color border (Line)
        backgroundColor: "#4CAF50", // Add custom color background (Points and Fill)
        borderWidth: 1, // Specify bar border width
      },
      {
        label: "User 3", // Name the series
        data: [
          10000, 7000, 1500, 4000, 3200, 7450, 5698, 7854, 6500, 7894, 4530,
          8634,
        ], // Specify the data values array
        fill: false,
        borderColor: "#000000", // Add custom color border (Line)
        backgroundColor: "#000000", // Add custom color background (Points and Fill)
        borderWidth: 1, // Specify bar border width
      },
    ],
  },
  options: {
    responsive: true, // Instruct chart js to respond nicely.
    maintainAspectRatio: false,
  },
});
