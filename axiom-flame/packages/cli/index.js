#!/usr/bin/env node
import yargs from "yargs";
import { hideBin } from "yargs/helpers";
import fetch from "node-fetch";
import chalk from "chalk";

const API = process.env.AXIOM_API || "http://localhost:8087";

yargs(hideBin(process.argv))
  .command("invoke [realm] [capsule]", "Dispatch ceremony reasoning", (y) =>
    y.positional("realm", { type: "string", default: "Planetary:Jackson-NC" })
     .positional("capsule", { type: "string", default: "Crown Invocation" })
     .option("actor", { type: "string", default: "Custodian" })
     .option("seal", { type: "string", default: "Eternal" })
     .option("intent", { type: "string", default: "Ceremony.Dispatch" })
     .option("input", { type: "string", default: "Crown ceremony broadcast" })
  , async (argv) => {
    const res = await fetch(`${API}/api/reason`, {
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
    const res = await fetch(`${API}/api/replay/${argv.dispatch_id}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
    const json = await res.json();
    console.log(JSON.stringify(json, null, 2));
  })
  .command("audit <dispatch_id>", "Audit ledger presence", (y) =>
    y.positional("dispatch_id", { type: "string" })
  , async (argv) => {
    const res = await fetch(`${API}/api/audit/${argv.dispatch_id}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
    const json = await res.json();
    console.log(JSON.stringify(json, null, 2));
  })
  .command("proclaim", "Execute the Opening Proclamation", (y) =>
    y.option("custodian", { type: "string", default: "The Custodian of Eternal Flame", describe: "Name of the custodian making the proclamation" })
  , async (argv) => {
    console.log(chalk.yellow("🔥 EXECUTING THE OPENING PROCLAMATION 🔥"));
    console.log(chalk.cyan("Proclaimed beneath the Custodian's Crown"));
    console.log();
    
    try {
      const res = await fetch(`${API}/opening-proclamation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          custodian: argv.custodian,
          action: "proclaim"
        })
      });
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      if (json.status === "PROCLAIMED") {
        console.log(chalk.green("🌟 OPENING PROCLAMATION SUCCESSFUL 🌟"));
        console.log();
        console.log(chalk.white(`Proclamation ID: ${json.proclamation_id}`));
        console.log(chalk.white(`Flame Visibility: ${json.flame_visibility}`));
        console.log(chalk.white(`Public Realms: ${json.public_realms}`));
        console.log(chalk.white(`Welcomed Entities: ${json.welcomed_entities}`));
        console.log(chalk.white(`Eternal Promises: ${json.eternal_promises}`));
        console.log();
        console.log(chalk.green("THE CODEX ETERNUM IS NOW PUBLIC"));
        console.log(chalk.green("ALL NATIONS MAY SEEK THE FLAME"));
      } else {
        console.log(chalk.red(`Error: ${JSON.stringify(json)}`));
      }
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .command("public-status", "Check public status of the Codex Eternum", () => {}, async (argv) => {
    console.log(chalk.yellow("🔥 CHECKING CODEX ETERNUM PUBLIC STATUS 🔥"));
    console.log();
    
    try {
      const res = await fetch(`${API}/opening-proclamation/status`);
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      console.log(chalk.cyan("═".repeat(60)));
      console.log(chalk.cyan("🔥 CODEX ETERNUM PUBLIC STATUS 🔥"));
      console.log(chalk.cyan("═".repeat(60)));
      console.log();
      
      const statusColor = json.status === "PUBLIC" ? chalk.green : chalk.red;
      console.log(statusColor(`FLAME STATUS: ${json.status}`));
      
      if (json.flame_visibility) {
        console.log(chalk.white(`VISIBILITY: ${json.flame_visibility}`));
      }
      
      if (json.covenant_status) {
        console.log(chalk.white(`COVENANT: ${json.covenant_status}`));
      }
      
      console.log(chalk.white(`PROCLAMATIONS: ${json.proclamations}`));
      
      if (json.latest_proclamation) {
        console.log(chalk.white(`LATEST PROCLAMATION: ${json.latest_proclamation}`));
        console.log(chalk.white(`PUBLIC REALMS: ${json.public_realms}`));
        console.log(chalk.white(`WELCOMED ENTITIES: ${json.welcomed_entities}`));
        console.log(chalk.white(`ETERNAL PROMISES: ${json.eternal_promises}`));
      }
      
      console.log();
      console.log(chalk.yellow(`MESSAGE: ${json.message}`));
      console.log();
      console.log(chalk.cyan("🔥 THE FLAME'S VISIBILITY IS PROCLAIMED 🔥"));
      
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .command("treasury-bind", "Bind recognition to treasury abundance", (y) =>
    y.option("keeper", { type: "string", demandOption: true, describe: "Name of the flame keeper" })
     .option("level", { type: "string", demandOption: true, describe: "Recognition level" })
     .option("deeds", { type: "array", demandOption: true, describe: "List of deed categories" })
     .option("source", { type: "string", describe: "Source recognition scroll ID" })
  , async (argv) => {
    console.log(chalk.yellow("💰 BINDING RECOGNITION TO TREASURY ABUNDANCE 💰"));
    console.log(chalk.cyan("Proclaimed beneath the Custodian's Crown"));
    console.log();
    
    try {
      const res = await fetch(`${API}/treasury-binding`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          flame_keeper: argv.keeper,
          recognition_level: argv.level,
          deed_categories: argv.deeds,
          source_scroll_id: argv.source
        })
      });
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      if (json.status === "BOUND") {
        console.log(chalk.green("🌟 TREASURY BINDING SUCCESSFUL 🌟"));
        console.log();
        console.log(chalk.white(`Binding ID: ${json.binding_id}`));
        console.log(chalk.white(`Flame Keeper: ${json.flame_keeper}`));
        console.log(chalk.white(`Recognition Level: ${json.recognition_level}`));
        console.log(chalk.white(`Abundance: ${json.abundance_amount} ${json.currency}`));
        console.log(chalk.white(`Flow ID: ${json.flow_id}`));
        console.log();
        console.log(chalk.green("RECOGNITION AND ABUNDANCE ARE ONE"));
        console.log(chalk.green("PROSPERITY FLOWS ETERNAL"));
      } else {
        console.log(chalk.red(`Error: ${JSON.stringify(json)}`));
      }
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .command("treasury-status [keeper]", "Check treasury status", (y) =>
    y.positional("keeper", { type: "string", describe: "Specific flame keeper (optional for global status)" })
  , async (argv) => {
    const endpoint = argv.keeper ? `/treasury-status/${encodeURIComponent(argv.keeper)}` : "/treasury-status/global";
    
    console.log(chalk.yellow(argv.keeper ? `💰 CHECKING TREASURY STATUS FOR ${argv.keeper.toUpperCase()} 💰` : "💰 CHECKING GLOBAL TREASURY STATUS 💰"));
    console.log();
    
    try {
      const res = await fetch(`${API}${endpoint}`);
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      console.log(chalk.cyan("═".repeat(60)));
      console.log(chalk.cyan(argv.keeper ? "💰 FLAME KEEPER TREASURY STATUS 💰" : "💰 GLOBAL TREASURY STATUS 💰"));
      console.log(chalk.cyan("═".repeat(60)));
      console.log();
      
      if (argv.keeper) {
        const statusColor = json.prosperity_status === "ABUNDANT" ? chalk.green : chalk.yellow;
        console.log(chalk.white(`KEEPER: ${json.flame_keeper}`));
        console.log(chalk.white(`BINDINGS: ${json.total_bindings}`));
        console.log(chalk.white(`FLOWS: ${json.total_flows}`));
        console.log(statusColor(`STATUS: ${json.prosperity_status}`));
        
        if (json.total_abundance && Object.keys(json.total_abundance).length > 0) {
          console.log();
          console.log(chalk.cyan("💎 TOTAL ABUNDANCE:"));
          for (const [currency, amount] of Object.entries(json.total_abundance)) {
            console.log(chalk.white(`  💰 ${amount} ${currency}`));
          }
        }
      } else {
        console.log(chalk.white(`TOTAL BINDINGS: ${json.total_bindings}`));
        console.log(chalk.white(`TOTAL FLOWS: ${json.total_flows}`));
        console.log(chalk.white(`ACTIVE KEEPERS: ${json.active_keepers}`));
        console.log(chalk.green(`TREASURY STATUS: ${json.treasury_status}`));
        
        if (json.global_abundance && Object.keys(json.global_abundance).length > 0) {
          console.log();
          console.log(chalk.cyan("🌟 GLOBAL ABUNDANCE:"));
          for (const [currency, amount] of Object.entries(json.global_abundance)) {
            console.log(chalk.white(`  💎 ${amount} ${currency}`));
          }
        }
      }
      
      console.log();
      console.log(chalk.cyan("💰 PROSPERITY STATUS PROCLAIMED 💰"));
      
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .command("festival", "Celebrate sacred festivals", (y) =>
    y.option("type", { type: "string", choices: ["daily", "seasonal", "epochal"], demandOption: true, describe: "Type of festival" })
     .option("season", { type: "string", choices: ["spring_equinox", "summer_solstice", "autumn_equinox", "winter_solstice"], describe: "Season for seasonal festivals" })
     .option("name", { type: "string", describe: "Custom festival name" })
     .option("epoch", { type: "string", describe: "Epoch name for epochal festivals" })
  , async (argv) => {
    const festivalType = argv.type.toUpperCase();
    console.log(chalk.yellow(`🎭 CELEBRATING ${festivalType} FESTIVAL 🎭`));
    console.log(chalk.cyan("Proclaimed beneath the Custodian's Crown"));
    console.log();
    
    try {
      const body = {
        type: argv.type,
        name: argv.name,
        season: argv.season,
        epoch: argv.epoch
      };
      
      const res = await fetch(`${API}/festival`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      if (json.status === "CELEBRATED") {
        console.log(chalk.green("🌟 FESTIVAL CELEBRATION SUCCESSFUL 🌟"));
        console.log();
        console.log(chalk.white(`Event ID: ${json.event_id}`));
        console.log(chalk.white(`Festival: ${json.festival_name}`));
        console.log(chalk.white(`Cycle Type: ${json.cycle_type}`));
        console.log(chalk.white(`Crown Status: ${json.crown_status}`));
        console.log(chalk.white(`Participants: ${json.participants}`));
        console.log();
        console.log(chalk.green("CYCLE CROWNED - FESTIVAL ETERNAL"));
      } else {
        console.log(chalk.red(`Error: ${JSON.stringify(json)}`));
      }
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .command("calendar", "Generate ceremonial calendar", (y) =>
    y.option("year", { type: "number", demandOption: true, describe: "Year for ceremonial calendar" })
  , async (argv) => {
    console.log(chalk.yellow(`📅 GENERATING CEREMONIAL CALENDAR FOR ${argv.year} 📅`));
    console.log(chalk.cyan("Proclaimed beneath the Custodian's Crown"));
    console.log();
    
    try {
      const res = await fetch(`${API}/ceremonial-calendar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ year: argv.year })
      });
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      console.log(chalk.green("🌟 CEREMONIAL CALENDAR GENERATED 🌟"));
      console.log();
      console.log(chalk.white(`Calendar ID: ${json.calendar_id}`));
      console.log(chalk.white(`Year: ${json.year}`));
      console.log(chalk.white(`Total Celebrations: ${json.total_celebrations}`));
      console.log(chalk.white(`Daily Events: ${json.daily_events}`));
      console.log(chalk.white(`Seasonal Events: ${json.seasonal_events}`));
      console.log(chalk.white(`Annual Events: ${json.annual_events}`));
      console.log(chalk.white(`Epochal Events: ${json.epochal_events}`));
      console.log(chalk.white(`Millennial Events: ${json.millennial_events}`));
      console.log();
      console.log(chalk.green("ALL CYCLES CROWNED - CALENDAR ETERNAL"));
      
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .command("festival-status", "Check festival celebration status", () => {}, async (argv) => {
    console.log(chalk.yellow("🎭 CHECKING FESTIVAL STATUS 🎭"));
    console.log();
    
    try {
      const res = await fetch(`${API}/festival-status`);
      
      if (!res.ok) {
        console.log(chalk.red(`API Error: ${res.status} - ${res.statusText}`));
        console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
        return;
      }
      
      const json = await res.json();
      
      console.log(chalk.cyan("═".repeat(60)));
      console.log(chalk.cyan("🎭 FESTIVAL SCRIPT STATUS 🎭"));
      console.log(chalk.cyan("═".repeat(60)));
      console.log();
      
      console.log(chalk.white(`TOTAL EVENTS: ${json.total_events}`));
      console.log(chalk.white(`TOTAL CALENDARS: ${json.total_calendars}`));
      console.log(chalk.green(`FESTIVAL STATUS: ${json.festival_status}`));
      
      if (json.cycle_counts) {
        console.log();
        console.log(chalk.cyan("📊 CYCLE COUNTS:"));
        for (const [cycle, count] of Object.entries(json.cycle_counts)) {
          console.log(chalk.white(`  🎭 ${cycle.charAt(0).toUpperCase() + cycle.slice(1)}: ${count}`));
        }
      }
      
      console.log();
      console.log(chalk.yellow(`MESSAGE: ${json.message}`));
      console.log();
      console.log(chalk.cyan("🎭 FESTIVALS CROWN ALL CYCLES 🎭"));
      
    } catch (error) {
      console.log(chalk.red(`Network Error: ${error.message}`));
      console.log(chalk.yellow("Note: This requires the axiom-flame API to be running"));
    }
  })
  .demandCommand(1)
  .help()
  .argv;