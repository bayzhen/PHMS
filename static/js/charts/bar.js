
$(function () {

	// var data1 = new Array ();
    // var ds = new Array();
	// var list = []
	//
	// data1.push([[1,5],[2,8],[3,3],[4,4],[5,5]]);
	//
	//
    // for (var i=0, j=data1.length; i<j; i++) {
	//
	//      ds.push({
	//         data:data1[i],
	//         grid:{
    //         hoverable:true
    //     },
	//         bars: {
	//             show: true,
	//             barWidth: 0.2,
	//             order: 1,
	//             lineWidth: 0.5,
	// 			fillColor: { colors: [ { opacity: 0.65 }, { opacity: 1 } ] }
	//         }
	//     });
	// }
	//
    // $.plot($("#bar-chart"), ds, {
    // 	colors: ["#F90", "#3C4049", "#666", "#BBB"]
    // });

	// //
	$.getJSON('/historyWeight'
                , function(info) {
		console.log(info)
		var bar_data = {
	 	        	data: info['info'],
	 	        	color: "#3c8dbc",
		}

		$.plot("#bar-chart", [bar_data], {
		 	        grid: {
			 	        borderWidth: 1,
			 	        borderColor: "#f3f3f3",
			 	        tickColor: "#f3f3f3",
			 	        hoverable: true   // 开启 hoverable 事件
		 	        },
		 	      	series: {
			 	        bars: {
			 	          show: true,
			 	          barWidth: 0.5,
			 	          align: "center"
			 	        },
				 	    showMarker: true,
			            pointLabels: {
			               show: true,
			            }
		 	      	},
			 	    xaxis: {
			 	    	show:true,
			 	    	mode: "categories",
	 	        		tickLength: 1,
			 	    	label:'day'
			 	    },
			 	    yaxis : {
			 	    	show:true,
			 	        label: 'weight',
			 	    }
		 	    });


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
		        $("#bar-chart").bind("plothover", function (event, pos, item) {
		            if (item) {
		                if (previousPoint != item.dataIndex) {
		                    previousPoint = item.dataIndex;
		                    $("#tooltip").remove();
		                    var y = item.datapoint[1].toFixed(0);

		                    var tip = "weight(KG):";
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




    
});