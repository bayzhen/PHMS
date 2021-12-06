$(function () {


    $.getJSON('/historyWeight'
                , function(info) {
		console.log(info);

		var plot = $.plot($("#line-chart"),
           [ { data: info['info']}], {
               series: {
                   lines: { show: true },
                   points: { show: true }
               },

               grid: { hoverable: true, clickable: true },
               yaxis : {
			 	    	show:true,
			 	        label: 'weight',
			 	    },
			   xaxis: {
			 	    	show:true,
			 	    	mode: "categories",
	 	        		tickLength: 1,
			 	    	label:'day'
			 	    },
    	colors: ["#F90", "#3C4049", "#666", "#BBB"]
             });
		// var bar_data = {
	 	//         	data: info['info'],
	 	//         	color: "#3c8dbc",
		// }
        //
		// $.plot("#bar-chart", [bar_data], {
		//  	        grid: {
		// 	 	        borderWidth: 1,
		// 	 	        borderColor: "#f3f3f3",
		// 	 	        tickColor: "#f3f3f3",
		// 	 	        hoverable: true   // 开启 hoverable 事件
		//  	        },
		//  	      	series: {
		// 	 	        bars: {
		// 	 	          show: true,
		// 	 	          barWidth: 0.5,
		// 	 	          align: "center"
		// 	 	        },
		// 		 	    showMarker: true,
		// 	            pointLabels: {
		// 	               show: true,
		// 	            }
		//  	      	},
		//
		//
		//  	    });


		      function showTooltip(x, y, contents) {
		            $('<div id="tooltip">' + contents + '</div>').css( {
		                position: 'absolute',
		                display: 'none',
		                top: y - 30,
		                left: x - 40,
		                padding: '2px',
		                'background-color': 'white',
		                opacity: 0.80
		            }).appendTo("body").fadeIn(200);
		        }

		        var previousPoint = null;
		        // 绑定提示事件
		        $("#line-chart").bind("plothover", function (event, pos, item) {
		            if (item) {
		                if (previousPoint != item.dataIndex) {
		                    previousPoint = item.dataIndex;
		                    $("#tooltip").remove();
		                    var y = item.datapoint[1].toFixed(0);

		                    var tip = "calorie(kcal):";
		                    showTooltip(item.pageX, item.pageY,tip+y);
		                }
		            }
		            else {
		                $("#tooltip").remove();
		                previousPoint = null;
		            }
		        });

	}
	)



    // var sin = [], cos = [];
    // for (var i = 0; i < 10; i += 0.5) {
    //     sin.push([i, Math.sin(i)]);
    //     cos.push([i, Math.cos(i)]);
    // }
    //
    // var plot = $.plot($("#line-chart"),
    //        [ { data: sin, label: "sin(x)"}, { data: cos, label: "cos(x)" } ], {
    //            series: {
    //                lines: { show: true },
    //                points: { show: true }
    //            },
    //
    //            grid: { hoverable: true, clickable: true },
    //            yaxis: { min: -1.1, max: 1.1 },
	// 		   xaxis: { min: 0, max: 9 },
    // 	colors: ["#F90", "#3C4049", "#666", "#BBB"]
    //          });
});