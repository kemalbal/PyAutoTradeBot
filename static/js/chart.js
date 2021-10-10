var chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: 2000,
    height: 350,
    layout: {
        backgroundColor: '#000000',
        textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    rightPriceScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
    timeScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
});

var candleSeries = chart.addCandlestickSeries({
    upColor: 'green',
    downColor: 'red',
    borderDownColor: 'red',
    borderUpColor: 'green',
    wickDownColor: 'red',
    wickUpColor: 'green',
});

var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      callback(status, xhr.response);
    };
    xhr.send();
};

getJSON('/history', (status, response) => {
    if(status === 200)
        candleSeries.setData(response);
});


getJSON('/trade', (status, response) => {
    if(status === 200)
    candleSeries.setMarkers(response);
});

