var options = {
  series: [
    {
      name: "Quantity (in L)",
      data: [15, 10, 17, 15, 23, 21, 30, 20, 26, 20, 28, 10],
    },
  ],
  chart: {
    height: 300,
    type: "line",
    zoom: {
      enabled: false,
    },
    dropShadow: {
      enabled: true,
      color: "#000",
      top: 18,
      left: 7,
      blur: 16,
      opacity: 0.2,
    },
    toolbar: {
      show: false,
    },
  },
  colors: ["#f0746c"],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    width: [3, 3],
    curve: "smooth",
  },
  grid: {
    show: false,
  },
  markers: {
    colors: ["#f0746c"],
    size: 5,
    strokeColors: "#ffffff",
    strokeWidth: 2,
    hover: {
      sizeOffset: 2,
    },
  },
  xaxis: {
    categories: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    labels: {
      style: {
        colors: "#8c9094",
      },
    },
  },
  yaxis: {
    min: 0,
    max: 35,
    labels: {
      style: {
        colors: "#8c9094",
      },
    },
  },
  legend: {
    position: "top",
    horizontalAlign: "right",
    floating: true,
    offsetY: 0,
    labels: {
      useSeriesColors: true,
    },
    markers: {
      width: 10,
      height: 10,
    },
  },
};

var options4 = {
  series: [89, 56, 78],
  chart: {
    height: 350,
    type: "radialBar",
  },
  colors: ["#003049", "#d62828", "#f77f00", "#fcbf49"],
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: {
          fontSize: "22px",
        },
        value: {
          fontSize: "16px",
        },
        total: {
          show: true,
          label: "Total",
          formatter: function (w) {
            return Math.round((223 / 300) * 100) + "%";
          },
        },
      },
    },
  },
  labels: ["pH", "Turbidity", "Temperature"],
};

var chart = new ApexCharts(
  document.querySelector("#activities-chart"),
  options
);
chart.render();

var chart4 = new ApexCharts(
  document.querySelector("#diseases-chart"),
  options4
);
chart4.render();

// datatable init
$("document").ready(function () {
  $(".data-table").DataTable({
    scrollCollapse: false,
    autoWidth: false,
    responsive: true,
    searching: false,
    bLengthChange: false,
    bPaginate: true,
    bInfo: false,
    columnDefs: [
      {
        targets: "datatable-nosort",
        orderable: false,
      },
    ],
    lengthMenu: [
      [5, 25, 50, -1],
      [5, 25, 50, "All"],
    ],
    language: {
      info: "_START_-_END_ of _TOTAL_ entries",
      searchPlaceholder: "Search",
      paginate: {
        next: '<i class="ion-chevron-right"></i>',
        previous: '<i class="ion-chevron-left"></i>',
      },
    },
  });
});
