var chart = c3.generate({
   data: {
       type:'bar',
        url: '/static/data.csv',
       bar: {
        width: {
        ratio: 0.1
    }
}
    },
    axis : {
        y: {
            label: {
            text: 'Price',
            position: 'outer-middle'
           },
            min: 130,
            max: 180
        },
        x:{
            type:'bar',
            tick:{
                format:'%Y-%m-%d'
            }
        }
    }
});
console.log(chart);