studio.menu.addMenuItem({ 
    name: "build ro project",
    execute: function() {
        var projectPath = studio.project.filePath
        var lastIndex  = projectPath.lastIndexOf('/');
        var folderPath = projectPath.substring(0, lastIndex);
        var pathToExecutable = folderPath + "/" + "move_files.bat"
        // Returns a result object { exitCode, standardOutput, standardError }.
        // var standardOutput = studio.system.start(pathToExecutable, {timeout: 20000, args: ["C:\\Users\\kenhuang\\Desktop\\SourceDes"]})
        studio.project.build();
        //输出txt文档 ============================================================================================================================================
        var allBankPath = studio.project.model.Bank.findInstances();
        var allbusPath = studio.project.model.MixerGroup.findInstances();
        //var allEventPath = studio.project.model.Event.findInstances();
        

        var headerFileName = "fmod_studio_info.txt"
        var outputPath = "";
        var folder = "";
        outputPath = folderPath + "/" +"Build/fmod_studio_info.txt";
        

        var textFile = studio.system.getFile(outputPath);
        
        if (!textFile.open(studio.system.openMode.WriteOnly)) {    
            alert("Failed to open file {0}\n\nCheck the file is not read-only.".format(outputPath));
            console.error("Failed to open file {0}.".format(outputPath));
            return;
        }
        
        textFile.writeText("Name,Type,Path,GUID,Nexessary Bank Name ,Bank Path,is3D" + "\n");
        allbusPath.forEach(function (each_bus){
            var buspath = each_bus.getPath();
            var busguid = each_bus.id;
            var bus_name_group = buspath.split('/');
            var bus_name_only = bus_name_group[bus_name_group.length - 1]
            textFile.writeText(bus_name_only + "," + "Bus" + "," + buspath +","+ busguid + "," + "Master" + "," + "bank:/Master" + "," +"None" +"\n");

        })
        allBankPath.forEach( function (each_bank) {
            each_bank.events.forEach(function(each_event){
                    var event_name = each_event.getPath();
                    var event_par_str = ""
                    //如果需要过滤掉某个字符串，例如event:
                    var name_group = event_name.split('/');
                    var event_name_only = name_group[name_group.length - 1]
                    var eventguid = each_event.id;
                    var event_bank_path = each_bank.getPath();
                    var bank_name_group = event_bank_path.split('/');
                    var bank_name_only = bank_name_group[bank_name_group.length - 1]
                    textFile.writeText(event_name_only + "," + "Event" + "," + event_name + "," +eventguid + "," + bank_name_only + "," + event_bank_path + "," + each_event.is3D() +"\n");
            } )
        });
        textFile.close();
        outputPath = outputPath.replace(/\//g, '\\')
        folder = folder.replace(/\//g, '\\')
        // ====================================================================================================================================================================
        //开始移动
        var standardOutput = studio.system.start(pathToExecutable, {timeout: 20000, args: [folderPath+"/Build",folderPath+"/../../Client_Editor/Assets/Editor/Resources/ArtRes/Bundle/Audio/FMOD"]})
        studio.system.startAsync("explorer", {workingdir: "", args: ["/open,",folder]});
        alert("Finished")
        // alert(standardOutput.standardOutput)
    }    
});
