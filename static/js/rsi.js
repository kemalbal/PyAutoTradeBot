var rsiElement = document.getElementById('rsi');

var rsi_chart = LightweightCharts.createChart(rsiElement, {
    width: 2000,
    height: 300,
    layout: {
        textColor: '#d1d4dc',
        backgroundColor: '#000000',
    },
    rightPriceScale: {
        scaleMargins: {
            top: 0.3,
            bottom: 0.25,
        },
    },
    crosshair: {
        vertLine: {
            width: 4,
            color: 'rgba(224, 227, 235, 0.1)',
            style: 0,
        },
        horzLine: {
            visible: false,
            labelVisible: false,
        },
    },
    grid: {
        vertLines: {
            color: 'rgba(42, 46, 57, 0)',
        },
        horzLines: {
            color: 'rgba(42, 46, 57, 0)',
        },
    },
    handleScroll: {
        vertTouchDrag: false,
    },
});
document.body.appendChild(rsiElement);

var series = rsi_chart.addLineSeries({
    color: 'rgb(0, 120, 255)',
    lineWidth: 2,
    crosshairMarkerVisible: false,
    lastValueVisible: false,
    priceLineVisible: false,
});

getJSON('/rsi', (status, response) => {
    if(status === 200)
    series.setData(response);
});

var lineWidth = 2;
var value30 = {
    price: 30,
    color: '#be1238',
    lineWidth: lineWidth,
    lineStyle: LightweightCharts.LineStyle.Solid,
    axisLabelVisible: true,
};
var value70 = {
    price: 70,
    color: '#be1238',
    lineWidth: lineWidth,
    lineStyle: LightweightCharts.LineStyle.Solid,
    axisLabelVisible: true,
}

series.createPriceLine(value30);
series.createPriceLine(value70);

rsi_chart.timeScale().fitContent();