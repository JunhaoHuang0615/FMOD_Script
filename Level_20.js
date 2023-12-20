/* -------------------------------------------
   FMOD Studio Script Example:
   Batch Rename Dialog
   -------------------------------------------
 */

   studio.menu.addMenuItem({
    name: "Level_20_sepprate_inproject",
    execute: function() {
        alert("This process will take a relatively long time. Pay attention to the progress in the bottom right corner. Do not close it halfway.")
        var model_bank_name = "VO_tha";
        var model_bus_name = "VO_tha";
        var target_bank_name = "VO_CNLive";
        var target_events_substring = "CV_CNLive";
        var target_bus_titleString = "VO_CNLive"
        var allEvents = studio.project.model.Event.findInstances();
        studio.ui.showModalDialog({
            windowTitle: "Level_20_seprate",
            windowWidth: 340,
            widgetType: studio.ui.widgetType.Layout,
            layout: studio.ui.layoutType.VBoxLayout,
            items: [
                { widgetType: studio.ui.widgetType.Label, text: "Input sample bank name" },
                { widgetType: studio.ui.widgetType.LineEdit, 
                    text: "VO_tha", 
                    widgetId: "m_filterText",
                    onTextEdited: function() 
                        {   
                            model_bank_name = this.findWidget("m_filterText").text();
                        } 
                },
                { widgetType: studio.ui.widgetType.Label, text: "Input head bus name of model bus" },
                { widgetType: studio.ui.widgetType.LineEdit, 
                    text: "VO_tha", 
                    widgetId: "m_filterTextmodelbus",
                    onTextEdited: function() 
                        {   
                            model_bus_name = this.findWidget("m_filterTextmodelbus").text();
                        } 
                },
                { widgetType: studio.ui.widgetType.Label, text: "Input target bank name" },
                { widgetType: studio.ui.widgetType.LineEdit, 
                    text: "VO_ida", 
                    widgetId: "m_filterTextTargetBankName",
                    onTextEdited: function() 
                        {   
                            target_bank_name = this.findWidget("m_filterTextTargetBankName").text();
                        } 
                },
                { widgetType: studio.ui.widgetType.Label, text: "Input target events subString " },
                { widgetType: studio.ui.widgetType.LineEdit, 
                    text: "CV_ida", 
                    widgetId: "m_filterText2",
                    onTextEdited: function() 
                        {   
                            target_events_substring = this.findWidget("m_filterText2").text();
                        } 
                },
                { widgetType: studio.ui.widgetType.Label, text: "Input head bus name you want generate" },
                { widgetType: studio.ui.widgetType.LineEdit, 
                    text: "VO_ida", 
                    widgetId: "target_events_substring",
                    onTextEdited: function() 
                        {   
                            target_bus_titleString = this.findWidget("target_events_substring").text();
                        } 
                },
                { widgetType: studio.ui.widgetType.PushButton, 
                    text: "Start", 
                    onClicked: function() 
                    {   
                        var allBank = studio.project.model.Bank.findInstances();
                        var allbus = studio.project.model.MixerGroup.findInstances();
                        // console(allbus[2].input[0].event.dump())
                        var target_events_list = []
                        //console(allbus[0].input[1].dump()) bus下的事件
                        //console(allbus[0].input[0].relationships.input.dump())
                        //allbus[0].input[0].relationships.input.dump()
                        var modelBank = null;
                        for(var i=0; i<allBank.length;i++){
                            if(allBank[i].getPath().indexOf(model_bank_name) > -1){
                                modelBank = allBank[i]
                            }
                        }
                        var target_Bank= null
                        for(var i=0; i<allBank.length;i++){
                            if(allBank[i].getPath().indexOf(target_bank_name) > -1){
                                target_Bank = allBank[i]
                            }
                        }
                        //获取目标事件（根据头路径名称，获取分类的事件）
                        allEvents.forEach(function(each_event){
                            if(each_event.getPath().indexOf(target_events_substring) > -1){
                                target_events_list.push(each_event)
                            }
                        })
                        //遍历模板Bank里面的所有事件，找到他们的名称
                        modelBank.events.forEach(function(each_event) {
                            //获取某个事件的最后一个名称：
                            var event_name_group = each_event.getPath().split("/");
                            var event_name = event_name_group[event_name_group.length - 1];
                            target_events_list.forEach(function(target_event) {
                                if(target_event.getPath().indexOf(event_name) > -1){
                                    target_Bank.relationships.events.add(target_event)
                                }
                            });
                        });
                        var modelbus = null;
                        //找到模板bus:
                        var flag = false;
                        allbus.forEach(function(eachbus){
                            if(eachbus.getPath().indexOf(model_bus_name) > -1){
                                if(flag == false){
                                    modelbus = eachbus;
                                    flag = true;
                                }
                            }
                        });
                        // for (const eachbus of allbus) {
                        //     if (modelbus) break; // 如果已经找到匹配的模型，则直接退出循环
                        //     if (eachbus.getPath().indexOf(model_bus_name) > -1) {
                        //         modelbus = eachbus;
                        //     }
                        // }
                        //遍历模板bus, 需要使用递归的方法创建bus
                        bus_mover(modelbus,target_bus_titleString,target_events_list,null)
                        //完成
                        alert("Done")

                    } 
                },
            ],
        });
    // allEventPath.forEach(function(element) {
    //     var eventPath = element.getPath();
    //     var eventGUID = element.id;
    //     var event_Bank = "";
    //     allBankPath.forEach(function(each_bank){
    //         each_bank.events.forEach(function(each_event){
    //             if(each_event.getPath() === element.getPath()){
    //                 event_Bank = each_bank.getPath()
    //             }
    //         })

    //     })
    //     textFile.writeText(eventPath + "," + eventGUID + "," + event_Bank + "\n");


    // });
},
});

function bus_mover(modelbus, createBusName , targetevents_list, parent_bus){
    var m_bus = studio.project.create("MixerGroup")
    m_bus.name = createBusName
    if(parent_bus != null){
        parent_bus.relationships.input.add(m_bus);
    }
    modelbus.input.forEach(function(each_input) {
        if(each_input.isOfType("MixerInput")){
            //首先找到它对应的event:
            var input_event = each_input.event;
            var input_event_name_group = input_event.getPath().split("/");
            var input_eventname = input_event_name_group[input_event_name_group.length - 1];
            targetevents_list.forEach(function(event){
                if(event.getPath().indexOf(input_eventname) > -1){
                    //需要放的这个bus内
                    m_bus.relationships.input.add(event.mixerInput);
                }
            });
        }
        else if(each_input.isOfType("MixerGroup")){
            //alert(each_input.name)
            bus_mover(each_input,each_input.name,targetevents_list,m_bus);
        }
    });
    // var m_bus = studio.project.create("MixerGroup") //创建bus
    // m_bus.name = "IamBus"
    // var anotherbus = studio.project.create("MixerGroup")
    // anotherbus.name = "dsadwqe";
    // m_bus.relationships.input.add(anotherbus)

            
    // bus.relationships.input.add(events[i].mixerInput); 使用这个方法来将某个事件放入到bus中

}