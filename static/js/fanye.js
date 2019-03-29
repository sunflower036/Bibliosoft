function goPage(pno,psize){		//psize调用时最好是偶数
	var itable = document.getElementById("idData");
	var num = itable.rows.length;//表格所有行数(所有记录数)
	console.log(num);
	var totalPage = 0;//总页数
	var pageSize = psize;//每页显示行数
	num -= 1;
	//总共分几页 
	if(num/pageSize > (parseInt(num/pageSize))){   
			totalPage=parseInt(num/pageSize)+1;   
	}else{   
		totalPage=parseInt(num/pageSize);   
	}   		
	var currentPage = pno;//当前页数
	var startRow = (currentPage - 1) * pageSize+1;//开始显示的行 
	var endRow = currentPage * pageSize;//结束显示的行 
	endRow = (endRow > num)? num : endRow;   
	console.log(endRow);
	//遍历显示数据实现分页
	for(var i=1;i<num+1;i++){    
		var irow = itable.rows[i];
		if(i>=startRow && i<=endRow){
			irow.style.display = "table-row";    //保证显示的宽度是自设的宽度
		}else{
			irow.style.display = "none";
		}
	}
	var pageEnd = document.getElementById("pageEnd");
	var tempStr = "Page: " + currentPage + " / " + totalPage + " , " + num +" records in all, ";
	// var tempStr = num+"条记录 分"+totalPage+"页 当前第"+currentPage+"页";
	if(currentPage>1){
		tempStr += "<a href=\"#\" onClick=\"goPage("+(1)+","+psize+")\"> Top Page </a>";
		tempStr += "<a href=\"#\" onClick=\"goPage("+(currentPage-1)+","+psize+")\">< Page Up&nbsp&nbsp</a>"
	}else{
		tempStr += " Top Page ";
		tempStr += " < Page Up&nbsp&nbsp";   
	}

	if(currentPage<totalPage){
		tempStr += "<a href=\"#\" onClick=\"goPage("+(currentPage+1)+","+psize+")\">  Page Down ></a>";
		tempStr += "<a href=\"#\" onClick=\"goPage("+(totalPage)+","+psize+")\"> End Page </a>";
	}else{
		tempStr += "  Page Down >";
		tempStr += " End Page";    
	}

	document.getElementById("barcon").innerHTML = tempStr;
// 	
// 	$("#itable").css('table-layout','fixed');
}