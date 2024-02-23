
export class FMODUtils {
    //fmod: FMOD = {};
    system: FMOD.StudioSystem = null;

    constructor() {
        // this.fmod = {
        //     TOTAL_MEMORY: 24 * 1024 * 1024,
        //     preRun: this.preRun,
        //     onRuntimeInitialized: this.main
        // };
        // FMODModule(this.fmod);
        this.InitFmod();
    }
    InitFmod() {
        var fmod: FMOD = {}
        fmod = {
            TOTAL_MEMORY: 24 * 1024 * 1024,
            preRun: () => {
                console.log('FMOD preRun. Mounting files...');
                //必须首先PreLoadFile，然后再下面去加载Bank
                fmod.FS_createPreloadedFile('/', 'Master.bank', 'F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/Master.bank', true, false);
                fmod.FS_createPreloadedFile('/', 'Master.strings.bank', 'F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/Master.strings.bank', true, false);
                fmod.FS_createPreloadedFile('/', 'BGM_combat_boss.bank', 'F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/BGM_combat_boss.bank', true, false);
            },
            onRuntimeInitialized: () => {
                console.log('Runtime Initialized!');
                let outval: any = {};
                fmod.Studio_System_Create(outval);
                let system = outval.val as FMOD.StudioSystem;
                system.initialize(128, FMOD.STUDIO_INITFLAGS.NORMAL, FMOD.INITFLAGS.NORMAL, null);

                system.loadBankFile('Master.strings.bank', FMOD.STUDIO_LOAD_BANK_FLAGS.NORMAL, outval);
                system.loadBankFile('Master.bank', FMOD.STUDIO_LOAD_BANK_FLAGS.NORMAL, outval);
                system.loadBankFile('BGM_combat_boss.bank', FMOD.STUDIO_LOAD_BANK_FLAGS.NORMAL, outval);


                system.getEvent('event:/BGM/BGM_combat_boss', outval);
                let desc = outval.val as FMOD.EventDescription;
                desc.createInstance(outval);
                let inst = outval.val as FMOD.EventInstance;
                inst.start();

                setInterval(() => {
                    system.update();
                }, 1000 / 60);
            }
        };
        FMODModule(fmod);

    }
    // preRun() {
    //     console.log('FMOD preRun. Mounting files...');
    //     console.log(this.fmod)
    //     this.fmod.FS_createPreloadedFile('/', 'Master.bank', 'F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/Master.bank', true, false);
    //     this.fmod.FS_createPreloadedFile('/', 'Master.strings.bank', 'F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/Master.strings.bank', true, false);
    // }


    public postEvent(event_path) {

    }
    // public main() {
    //     console.log('Runtime Initialized!');
    //     let outval: any = {};
    //     this.fmod.Studio_System_Create(outval);
    //     this.system = outval.val as FMOD.StudioSystem;

    //     this.system.initialize(128, FMOD.STUDIO_INITFLAGS.NORMAL, FMOD.INITFLAGS.NORMAL, null);

    //     this.system.loadBankFile('F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/Master.strings.bank', FMOD.STUDIO_LOAD_BANK_FLAGS.NORMAL, outval);
    //     this.system.loadBankFile('F:/JJSG/client/client_laya/bin/res/fspriteassets/FmodBanks/BGM_combat_boss.bank', FMOD.STUDIO_LOAD_BANK_FLAGS.NORMAL, outval);

    //     this.system.getEvent('event:/BGM/BGM_combat_boss', outval);
    //     let desc = outval.val as FMOD.EventDescription;
    //     desc.createInstance(outval);
    //     let inst = outval.val as FMOD.EventInstance;
    //     inst.start();

    //     setInterval(() => {
    //         this.system.update();
    //     }, 1000 / 60);

    // }
}
