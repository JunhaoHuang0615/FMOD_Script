/* -------------------------------------------
   FMOD Studio Script Example:
   Batch Rename Dialog
   -------------------------------------------
 */

   studio.menu.addMenuItem({
    name: "Custom/Export event csv",
    execute: function() {
        var allBankPath = studio.project.model.Bank.findInstances();
        var allEventPath = studio.project.model.Event.findInstances();

        var headerType = "csv";
        var headerFileName = "fmod_studio_events.csv"
        var outputPath = studio.project.filePath;
        var projectName = outputPath.substr(outputPath.lastIndexOf("/") + 1, outputPath.length);
        outputPath = outputPath.substr(0, outputPath.lastIndexOf("/") + 1) + headerFileName;

    var textFile = studio.system.getFile(outputPath);
    if (!textFile.open(studio.system.openMode.WriteOnly)) {    
        alert("Failed to open file {0}\n\nCheck the file is not read-only.".format(outputPath));
        console.error("Failed to open file {0}.".format(outputPath));
        return;
    }
    
    textFile.writeText("Events Path,GUID,Bank Path" + "\n");
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
    allBankPath.forEach( function (each_bank) {
        each_bank.events.forEach(function(each_event){
             var event_name = each_event.getPath();
             var eventguid = each_event.id;
             var event_bank_path = each_bank.getPath();
             textFile.writeText(event_name + "," + eventguid + "," + event_bank_path + "\n");

        } )
    });
    textFile.close();

    alert("file successfully created at:\n\n{1}".format(outputPath));
    console.log("Header file successfully created at: " + outputPath);
    },
});
