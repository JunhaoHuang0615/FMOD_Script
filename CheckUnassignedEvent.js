// 添加菜单项
studio.menu.addMenuItem({
    name: "CheckEvents Unassigned",
    execute: checkEvent  
  });
  
  // 显示对话框
  function checkEvent() {

    var exception_string = "HotFix"

    studio.ui.showModalDialog({
        windowTitle: "CheckEventNotInBank",
        windowWidth: 340,
        widgetType: studio.ui.widgetType.Layout,
        layout: studio.ui.layoutType.VBoxLayout,
        items: [
            { widgetType: studio.ui.widgetType.Label, text: "Please input containing string of the excepted banks" },
            { widgetType: studio.ui.widgetType.LineEdit, 
                text: "HotFix", 
                widgetId: "m_filterText",
                onTextEdited: function() 
                    {   
                        exception_string = this.findWidget("m_filterText").text();
                    } 
            },
            { widgetType: studio.ui.widgetType.Label, text: "Check in Bank" },
            { widgetType: studio.ui.widgetType.PushButton, 
                text: "check unassigned events", 
                onClicked: function() 
                    {   
                        var allBankPath = studio.project.model.Bank.findInstances();
                        var bank_dict = []
                        allBankPath.forEach(function(element) {
                            bank_dict.push(element.getPath())
                        });
                        var allEventPath = studio.project.model.Event.findInstances();
                        var bank_combo = [{text: "Select Bank"}]
                        bank_dict.forEach(function(element) {
                            bank_combo.push({text: element})
                        });

                        var bank_path_instance_dict = {}
                        allBankPath.forEach(function(element) {
                            bank_path_instance_dict[element.getPath()] = element;
                        });
                        //遍历所有的事件
                        var bank_withouthotfix = []
                        allBankPath.forEach(function(element) {
                            if(element.getPath().indexOf(exception_string) > -1){
                                
                            }
                            else{
                                bank_withouthotfix.push(element);
                                //alert(element.getPath())
                            }
                        });
                        
                        var alert_text = "";
                        var event_list = []
                        allEventPath.forEach(function(element) {
                            //查看他们所在的bank
                            flag = true;
                            bank_withouthotfix.forEach(function(bank_ins){
                                bank_ins.events.forEach(function(bank_event){
                                    if(element.getPath()+"" === bank_event.getPath()+""){
                                        //在非HotFix的Bank中可以找到
                                        flag = false;
                                    }
                                })
                            }); 
                            if(flag){
                                alert_text = alert_text + element.getPath() + "\n";
                                event_list.push(element);  
                            }
                        });
                        if(alert_text === ""){
                            alert("events have been successfully assigned");
                        }
                        else{
                            //绘制事件名称以及要加入的Bank
                            //打开添加事件的界面：========================================================================
                            ui_window_list = []
                            var index = 0;
                            ui_window_list.push({});
                            ui_window_list[index].windowTitle = "Add Event To Bank";
                            ui_window_list[index].windowWidth = 340;
                            ui_window_list[index].widgetType = studio.ui.widgetType.Layout;
                            ui_window_list[index].layout = studio.ui.layoutType.VBoxLayout;
                            ui_window_list[index].items = []
                            
                            var count = 0;
                            var ComboBox_index = 0;
                            event_list.forEach(function(event_ins){
                                if(count > 10){
                                    index = index + 1;
                                    ui_window_list.push({});
                                    ui_window_list[index].windowTitle = "Add Event To Bank";
                                    ui_window_list[index].windowWidth = 340;
                                    ui_window_list[index].widgetType = studio.ui.widgetType.Layout;
                                    ui_window_list[index].layout = studio.ui.layoutType.VBoxLayout;
                                    ui_window_list[index].items = []
                                    count = -1;
                                }
                                var layout_dict = {}

                                layout_dict.widgetType = studio.ui.widgetType.Layout;
                                layout_dict.layout = studio.ui.layoutType.HBoxLayout,
                                layout_dict.items = []
                                layout_dict.items.push({ widgetType: studio.ui.widgetType.Label, text: event_ins.getPath() })
                                //checkbox:选择要加入的bank
                                layout_dict.items.push({
                                    widgetType: studio.ui.widgetType.ComboBox,
                                    widgetId: event_ins.getPath(),
                                    items: bank_combo,
                                    currentIndex: 0,
                                    onCurrentIndexChanged: function() { AddtoBank(this, event_ins,bank_path_instance_dict,exception_string); },
                                })
                                ui_window_list[index].items.push(layout_dict);
                                count = count + 1;
                                ComboBox_index = ComboBox_index + 1;
                                //alert(layout_dict.items[1]['widgetId'])
                            })
                            ui_window_list.forEach(function(ui_window){

                                studio.ui.showModalDialog(ui_window);
                            })
                        }
                        
                        // temp_result.forEach(function(element){
                        //     tempselectEvent.
                        // })
                        
                    } 
            },
        ],
    });
  }

  function AddtoBank(widget,event_ins,bank_path_instance_dict,exception_string){
    if(widget.findWidget(event_ins.getPath()).currentIndex() != 0){
        //需要首先移除之前加入的Bank
        var allBankIns = studio.project.model.Bank.findInstances();
        allBankIns.forEach(function(each_bankins){
            if(each_bankins.getPath().indexOf(exception_string)>-1){
                //放到HotFix的不管
            }else{
                each_bankins.events.forEach(function(event){
                    if(event.getPath() === event_ins.getPath()){
                        //先从bank中移除
                        each_bankins.relationships.events.remove(event_ins);
                    }
                })
            }
        });
        bankpath = widget.findWidget(event_ins.getPath()).currentText()
        bankins = bank_path_instance_dict[bankpath];
        //将事件添加进入Bank里面： 参考 https://qa.fmod.com/t/a-question-about-scripts-such-as-add-group-track-js/15514
        bankins.relationships.events.add(event_ins);
    }

  }