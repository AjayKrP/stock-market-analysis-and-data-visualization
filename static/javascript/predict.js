var chart = c3.generate({
    bindto:'#chart',
    data: {
        x: 'Date',
        x_format : '%Y-%m-%d',
        url: '/static/data.csv'
    },
    axis : {
        x : {
            type : 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
        }
    }
});