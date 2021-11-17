 var cnt=0;
document.getElementById("add").onclick = function()
{
  var year = document.getElementById('year').value;
  if((year==1||year==2||year==3||year==4)&&cnt==0)
  {
      cnt++;
      var select = document.createElement("select");
      select.name = "semester";
      select.id = "semester";
      select.class = "form-control col-sm-10";
      if(year==1)
      {
            var sems = [1,2];
            for(const sem of sems)
            {
                var option = document.createElement("option");
                option.value = sem;
                option.text = "Sem "+sem.toString();
                select.appendChild(option);
            }
       }
        if(year==2)
        {
            var sems = [3,4];
            for(const sem of sems)
            {
                var option = document.createElement("option");
                option.value = sem;
                option.text = "Sem "+sem.toString();
                select.appendChild(option);
            }
        }
        if(year==3)
        {
            var sems = [5,6];
            for(const sem of sems)
            {
                var option = document.createElement("option");
                option.value = sem;
                option.text = "Sem "+sem.toString();
                select.appendChild(option);
            }
        }
        if(year==4)
        {
            var sems = [7,8];
            for(const sem of sems)
            {
                var option = document.createElement("option");
                option.value = sem;
                option.text = "Sem "+sem.toString();
                select.appendChild(option);
            }
        }
        var label = document.createElement("label");
        label.innerHTML = ""
        label.htmlFor = "semester";
        label.class = "control-label col-sm-2";
        document.getElementById("container").appendChild(label).appendChild(select);
    }
  }




