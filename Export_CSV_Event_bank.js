/* -------------------------------------------
   FMOD Studio Script Example:
   Batch Rename Dialog
   -------------------------------------------
 */

   studio.menu.addMenuItem({
    name: "Export event csv",
    execute: function() {
        var path = "";
        studio.ui.showModalDialog({
            windowTitle: "Export CSV File",
            windowWidth: 340,
            widgetType: studio.ui.widgetType.Layout,
            layout: studio.ui.layoutType.VBoxLayout,
            items: [
                { 
                    windowTitle: "Open a file",
                    widgetType: studio.ui.widgetType.PathLineEdit,
	                text: "",
	                label: "Please select a file to open and close the window when done",
                    pathType: studio.ui.pathType.Directory,
	                onEditingFinished: function() 
                    {
		                path = this.text(); 
                    },
                },
                { widgetType: studio.ui.widgetType.Label, text: "Export CSV" },
                { widgetType: studio.ui.widgetType.PushButton, 
                    text: "Export CSV File", 
                    onClicked: function() 
                    {   
                        var allBankPath = studio.project.model.Bank.findInstances();
                        //var allEventPath = studio.project.model.Event.findInstances();

                        var headerType = "csv";
                        var headerFileName = "fmod_studio_events.csv"
                        var outputPath = "";
                        var folder = "";
                        if(path === ""){
                            outputPath = studio.project.filePath;
                            // var projectName = outputPath.substr(outputPath.lastIndexOf("/") + 1, outputPath.length);
                            folder = outputPath.substr(0, outputPath.lastIndexOf("/") + 1)
                            outputPath = folder + headerFileName;
                        }
                        else{
                            folder = path;
                            outputPath = path + "/" +headerFileName;
                        }

                        var textFile = studio.system.getFile(outputPath);
                        
                        if (!textFile.open(studio.system.openMode.WriteOnly)) {    
                            alert("Failed to open file {0}\n\nCheck the file is not read-only.".format(outputPath));
                            console.error("Failed to open file {0}.".format(outputPath));
                            return;
                        }
                        
                        textFile.writeText("Event name,Event Path,GUID,Bank Path" + "\n");
                        allBankPath.forEach( function (each_bank) {
                            each_bank.events.forEach(function(each_event){
                                 var event_name = each_event.getPath();
                                 //如果需要过滤掉某个字符串，例如event:
                                 var name_group = event_name.split('/');
                                 var event_name_only = name_group[name_group.length - 1]
                                 var eventguid = each_event.id;
                                 var event_bank_path = each_bank.getPath();
                                 textFile.writeText(event_name_only + "," + event_name.replace(/^event:/, '') + "," + eventguid + "," + event_bank_path.replace(/^bank:/, '') + "\n");
                    
                            } )
                        });
                        textFile.close();
                    
                        //alert("Export Successed!" + outputPath)
                        outputPath = outputPath.replace(/\//g, '\\')
                        folder = folder.replace(/\//g, '\\')
                        
                        alert("Export Successed!" + outputPath)
                        // /open, F:\git_backup
                        // studio.system.startAsync("explorer", {workingdir: "", args: ["/open,",outputPath]});
                        studio.system.startAsync("explorer", {workingdir: "", args: ["/open,",folder]});
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
