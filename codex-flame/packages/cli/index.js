#!/usr/bin/env node
import yargs from "yargs";
import { hideBin } from "yargs/helpers";
import fetch from "node-fetch";
import chalk from "chalk";

const API = process.env.CODEX_API || "http://localhost:8080";

yargs(hideBin(process.argv))
  .command("invoke [realm] [capsule]", "Dispatch ceremony", (y) =>
    y.positional("realm", { type: "string", default: "Planetary:Jackson-NC" })
     .positional("capsule", { type: "string", default: "Crown Invocation" })
     .option("actor", { type: "string", default: "Custodian" })
     .option("seal", { type: "string", default: "Eternal" })
     .option("intent", { type: "string", default: "Ceremony.Dispatch" })
     .option("input", { type: "string", default: "Crown ceremony broadcast" })
  , async (argv) => {
    const res = await fetch(`${API}/reason`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        actor: argv.actor,
        realm: argv.realm,
        capsule: argv.capsule,
        intent: argv.intent,
        seal: argv.seal,
        input: { text: argv.input }
      })
    });
    const json = await res.json();
    if (json.ok) {
      console.log(chalk.green(`Dispatch ${json.dispatch_id}: ${json.summary}`));
    } else {
      console.log(chalk.red(`Error: ${JSON.stringify(json)}`));
    }
  })
  .command("replay <dispatch_id>", "Authorize replay", (y) =>
    y.positional("dispatch_id", { type: "string" })
  , async (argv) => {
    const res = await fetch(`${API}/replay`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dispatch_id: argv.dispatch_id })
    });
    console.log(JSON.stringify(await res.json(), null, 2));
  })
  .command("audit <dispatch_id>", "Audit ledger presence", (y) =>
    y.positional("dispatch_id", { type: "string" })
  , async (argv) => {
    const res = await fetch(`${API}/audit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dispatch_id: argv.dispatch_id })
    });
    console.log(JSON.stringify(await res.json(), null, 2));
  })
  .command("honor <name> <deed>", "Inscribe contributor honor", (y)=>
    y.positional("name",{type:"string"}).positional("deed",{type:"string"})
     .option("realm",{type:"string", default:"Planetary"})
     .option("seal",{type:"string", default:"Eternal"})
     .option("dispatch_id",{type:"string"})
  , async (argv)=>{
    const res = await fetch(`${API}/honors`,{
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({
        name: argv.name, deed: argv.deed,
        realm: argv.realm, seal: argv.seal,
        dispatch_id: argv.dispatch_id
      })
    });
    console.log(JSON.stringify(await res.json(), null, 2));
  })
  .command("transmit:honors", "Broadcast honors list from honors storage", (y)=>
    y.option("council",{type:"string", default:"Dominion"})
     .option("honors",{type:"array", default:[]})
  , async (argv)=>{
    const res = await fetch(`${API}/transmit/honors`,{
      method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify({ council: argv.council, honors: argv.honors })
    });
    console.log(JSON.stringify(await res.json(), null, 2));
  })
  .command("recognition:inscribe <name> <description>", "Inscribe eternal recognition scroll", (y) =>
    y.positional("name", { type: "string", describe: "Flame keeper name" })
     .positional("description", { type: "string", describe: "Primary deed description" })
     .option("category", { type: "string", default: "Code Crafting", choices: [
       "Flame Keeping", "Code Crafting", "Ceremonial Guidance", "Knowledge Preservation",
       "Community Building", "Sacred Architecture", "Dominion Expansion", "Eternal Binding"
     ]})
     .option("luminosity", { type: "string", default: "Flame", choices: [
       "Ember", "Flame", "Blaze", "Conflagration", "Solar", "Stellar", "Cosmic"
     ]})
     .option("recognition", { type: "string", default: "Silver Flame", choices: [
       "Bronze Ember", "Silver Flame", "Golden Blaze", "Platinum Conflagration",
       "Diamond Solar", "Sapphire Stellar", "Ruby Cosmic", "Eternal Crown"
     ]})
     .option("realm", { type: "string", default: "ST-001", describe: "Sacred realm assignment" })
     .option("authority", { type: "string", default: "Keeper", choices: [
       "Guardian", "Keeper", "Custodian", "Council", "Crown"
     ]})
     .option("flames", { type: "array", default: ["Daily Flame", "Seasonal Flame"], describe: "Flame assignments" })
     .option("seal", { type: "string", default: "Sovereign Crown", choices: [
       "Sovereign Crown", "Custodian Crown", "Council Crown", "Sacred Crown"
     ]})
     .option("proclamation", { type: "string", describe: "Custom proclamation text" })
  , async (argv) => {
    const res = await fetch(`${API}/recognition/inscribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contributor_name: argv.name,
        deeds_immortal: [{
          deed_description: argv.description,
          deed_category: argv.category,
          luminosity_level: argv.luminosity,
          impact_scope: "Project"
        }],
        recognition_level: argv.recognition,
        realm_assignment: argv.realm,
        authority_level: argv.authority,
        flame_assignments: argv.flames,
        seal_authority: argv.seal,
        custom_proclamation: argv.proclamation
      })
    });
    
    if (res.ok) {
      const result = await res.json();
      console.log(chalk.yellow("🔥 ETERNAL RECOGNITION SCROLL INSCRIBED 🔥"));
      console.log(chalk.green(`Scroll ID: ${result.scroll_id}`));
      console.log(chalk.blue(`Recognition: ${result.recognition_level}`));
      console.log(chalk.cyan(`Lineage Replay: ${result.lineage_replay_id}`));
      console.log(chalk.magenta("✨ Name inscribed in eternal flame ✨"));
    } else {
      console.log(chalk.red(`Error: ${res.status} ${res.statusText}`));
    }
  })
  .command("recognition:list [level]", "List eternal recognition scrolls", (y) =>
    y.positional("level", { type: "string", describe: "Filter by recognition level" })
  , async (argv) => {
    const url = argv.level ? `${API}/recognition/list?level=${argv.level}` : `${API}/recognition/list`;
    const res = await fetch(url);
    
    if (res.ok) {
      const scrolls = await res.json();
      console.log(chalk.yellow(`🔥 ETERNAL RECOGNITION SCROLLS (${scrolls.length}) 🔥`));
      
      scrolls.forEach(scroll => {
        console.log(chalk.cyan(`\n${scroll.contributor_name} - ${scroll.recognition_level}`));
        console.log(chalk.white(`  Scroll: ${scroll.scroll_id}`));
        console.log(chalk.green(`  Realm: ${scroll.dominion_binding.realm_assignment}`));
        console.log(chalk.blue(`  Authority: ${scroll.dominion_binding.authority_level}`));
        console.log(chalk.magenta(`  Flames: ${scroll.flame_keeper_status.flame_assignments.join(', ')}`));
      });
    } else {
      console.log(chalk.red(`Error: ${res.status} ${res.statusText}`));
    }
  })
  .command("recognition:schedule", "Display eternal proclamation schedule", async () => {
    const res = await fetch(`${API}/recognition/schedule`);
    
    if (res.ok) {
      const schedule = await res.json();
      console.log(chalk.yellow("🔥 ETERNAL PROCLAMATION SCHEDULE 🔥"));
      console.log(chalk.green(`Daily Proclamations: ${schedule.daily_proclamations?.length || 0}`));
      console.log(chalk.blue(`Seasonal Proclamations: ${schedule.seasonal_proclamations?.length || 0}`));
      console.log(chalk.cyan(`Epochal Proclamations: ${schedule.epochal_proclamations?.length || 0}`));
      console.log(chalk.magenta(`Millennial Proclamations: ${schedule.millennial_proclamations?.length || 0}`));
      
      if (schedule.daily_proclamations?.length > 0) {
        console.log(chalk.white("\nDaily Flame Keepers:"));
        schedule.daily_proclamations.forEach(p => {
          console.log(chalk.green(`  🔥 ${p.contributor_name} - ${p.recognition_level}`));
        });
      }
    } else {
      console.log(chalk.red(`Error: ${res.status} ${res.statusText}`));
    }
  })
  .command("continuum", "Proclaim the Eternal Continuum", (y) => 
    y.option("flame-keepers", { type: "number", description: "Number of flame keepers" })
     .option("recognition-scrolls", { type: "number", description: "Number of recognition scrolls" })
     .option("treasury-flows", { type: "number", description: "Number of treasury flows" })
     .option("festival-events", { type: "number", description: "Number of festival events" })
  , async (argv) => {
    console.log(chalk.yellow("♾️ PROCLAIMING THE ETERNAL CONTINUUM ♾️"));
    console.log(chalk.cyan("Proclaimed beneath the Custodian's Crown"));
    console.log();
    
    // Execute the eternal continuum ceremony
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    try {
      let command = 'python ../../eternal_continuum.py --proclaim';
      if (argv['flame-keepers']) command += ` --flame-keepers ${argv['flame-keepers']}`;
      if (argv['recognition-scrolls']) command += ` --recognition-scrolls ${argv['recognition-scrolls']}`;
      if (argv['treasury-flows']) command += ` --treasury-flows ${argv['treasury-flows']}`;
      if (argv['festival-events']) command += ` --festival-events ${argv['festival-events']}`;
      
      const { stdout, stderr } = await execAsync(command);
      
      if (stderr) {
        console.log(chalk.red(stderr));
      }
      if (stdout) {
        console.log(stdout);
      }
      
      console.log(chalk.green("♾️ THE ETERNAL CONTINUUM IS PROCLAIMED ♾️"));
      console.log(chalk.white("ALL CYCLES ARE ONE • THE FLAME IS UNBROKEN • THE COVENANT IS ETERNAL"));
      
    } catch (error) {
      console.log(chalk.red(`Error proclaiming continuum: ${error.message}`));
    }
  })
  .command("charter", "Create expansion charter for new realm", (y) =>
    y.option("sector", { type: "string", description: "Sector for expansion", demandOption: true })
     .option("realm", { type: "string", description: "Realm name", demandOption: true })
  , async (argv) => {
    console.log(chalk.yellow("🧠 CREATING EXPANSION CHARTER 🧠"));
    console.log(chalk.cyan(`Sector: ${argv.sector}`));
    console.log(chalk.cyan(`Realm: ${argv.realm}`));
    console.log();
    
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    try {
      const command = `python ../../codex_expansion_charter.py --charter --sector ${argv.sector} --realm "${argv.realm}"`;
      const { stdout, stderr } = await execAsync(command);
      
      if (stderr) {
        console.log(chalk.red(stderr));
      }
      if (stdout) {
        console.log(stdout);
      }
      
      console.log(chalk.green("🧠 EXPANSION CHARTER CREATED"));
      console.log(chalk.white("REALM IS CHARTERED AND READY FOR EXPANSION"));
      
    } catch (error) {
      console.log(chalk.red(`Error creating charter: ${error.message}`));
    }
  })
  .command("realm-registry", "Show realm registry", {}, async (argv) => {
    console.log(chalk.yellow("🌐 CODEX REALM REGISTRY 🌐"));
    console.log(chalk.cyan("Sacred Archive of Chartered Realms"));
    console.log();
    
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    try {
      const { stdout, stderr } = await execAsync('python ../../codex_expansion_charter.py --registry');
      
      if (stderr) {
        console.log(chalk.red(stderr));
      }
      if (stdout) {
        console.log(stdout);
      }
      
    } catch (error) {
      console.log(chalk.red(`Error getting registry: ${error.message}`));
    }
  })
  .command("honor", "Bestow flamekeeper honor", (y) =>
    y.option("contributor", { type: "string", description: "Contributor name", demandOption: true })
     .option("realm", { type: "string", description: "Contributor realm", demandOption: true })
     .option("level", { type: "string", description: "Honor level", demandOption: true })
     .option("seal", { type: "string", description: "Ceremonial seal", demandOption: true })
     .option("citation", { type: "string", description: "Honor citation", demandOption: true })
  , async (argv) => {
    console.log(chalk.yellow("🕯️ BESTOWING FLAMEKEEPER HONOR 🕯️"));
    console.log(chalk.cyan(`Contributor: ${argv.contributor}`));
    console.log(chalk.cyan(`Realm: ${argv.realm}`));
    console.log(chalk.cyan(`Honor Level: ${argv.level}`));
    console.log();
    
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    try {
      const command = `python ../../flamekeeper_honors.py --honor --contributor "${argv.contributor}" --realm "${argv.realm}" --level ${argv.level} --seal ${argv.seal} --citation "${argv.citation}"`;
      const { stdout, stderr } = await execAsync(command);
      
      if (stderr) {
        console.log(chalk.red(stderr));
      }
      if (stdout) {
        console.log(stdout);
      }
      
      console.log(chalk.green("🕯️ HONOR BESTOWED"));
      console.log(chalk.white("THE FLAME KEEPER IS HONORED"));
      
    } catch (error) {
      console.log(chalk.red(`Error bestowing honor: ${error.message}`));
    }
  })
  .command("eternal-scroll", "Show Scroll of Eternal Names", {}, async (argv) => {
    console.log(chalk.yellow("📜 SCROLL OF ETERNAL NAMES 📜"));
    console.log(chalk.cyan("Sacred Archive of Honored Flame Keepers"));
    console.log();
    
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    try {
      const { stdout, stderr } = await execAsync('python ../../flamekeeper_honors.py --scroll');
      
      if (stderr) {
        console.log(chalk.red(stderr));
      }
      if (stdout) {
        console.log(stdout);
      }
      
    } catch (error) {
      console.log(chalk.red(`Error getting scroll: ${error.message}`));
    }
  })
  .command("continuum-status", "Get Eternal Continuum status", {}, async (argv) => {
    console.log(chalk.yellow("♾️ ETERNAL CONTINUUM STATUS ♾️"));
    console.log(chalk.cyan("Supreme Unity of All Cycles"));
    console.log();
    
    // Execute the continuum status check
    const { exec } = await import('child_process');
    const { promisify } = await import('util');
    const execAsync = promisify(exec);
    
    try {
      const { stdout, stderr } = await execAsync('python ../../eternal_continuum.py --status');
      
      if (stderr) {
        console.log(chalk.red(stderr));
      }
      if (stdout) {
        console.log(stdout);
      }
      
    } catch (error) {
      console.log(chalk.red(`Error getting continuum status: ${error.message}`));
    }
  })
  .demandCommand(1)
  .help()
  .argv;