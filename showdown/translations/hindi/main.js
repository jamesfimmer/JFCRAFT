"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var main_exports = {};
__export(main_exports, {
  translations: () => translations
});
module.exports = __toCommonJS(main_exports);
const translations = {
  name: "Hindi",
  strings: {
    "namelocked": "namelocked",
    "locked": "locked",
    "autoconfirmed": "autoconfirmed",
    "trusted": "\u0935\u093F\u0936\u094D\u0935\u0938\u0928\u0940\u092F",
    "Please follow the rules:": "\u0915\u0943\u092A\u092F\u093E \u0907\u0928 \u0928\u093F\u092F\u092E\u094B\u0902 \u0915\u093E \u092A\u093E\u0932\u0928 \u0915\u0930\u0947\u0902:",
    "[TN: Link to the PS rules for your language (path after pokemonshowdown.com]/rules": "/pages/rules-hi",
    "Global Rules": "\u0938\u093E\u092E\u093E\u0928\u094D\u092F \u0928\u093F\u092F\u092E",
    "${room} room rules": "${room} Room \u0915\u0947 \u0928\u093F\u092F\u092E",
    "<strong>Global ranks</strong>": "<strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 \u092A\u0926</strong>",
    "+ <strong>Global Voice</strong> - They can use ! commands like !groups": "+ <strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 Voice</strong> - \u092F\u0947 \u0932\u094B\u0917 '!' commands \u0915\u093E \u0907\u0938\u094D\u0924\u0947\u092E\u093E\u0932 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902, \u091C\u0948\u0938\u0947 \u0915\u0940 !groups",
    "% <strong>Global Driver</strong> - The above, and they can also lock users and check for alts": "% <strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 Driver</strong> - \u092F\u0947 \u0932\u094B\u0917 \u090A\u092A\u0930 \u0915\u0940 \u091A\u0940\u091C\u093C\u0947\u0902 \u0914\u0930 \u0909\u0938\u0915\u0947 \u0905\u0932\u093E\u0935\u093E lock \u092F\u093E alt \u092D\u0940 \u091C\u093E\u0901\u091A \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",
    "@ <strong>Global Moderator</strong> - The above, and they can globally ban users": "@ <strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 Moderator</strong> - \u092F\u0947 \u0932\u094B\u0917 \u090A\u092A\u0930 \u0915\u0940 \u091A\u0940\u091C\u093C\u0947\u0902 \u0914\u0930 \u0909\u0938\u0915\u0947 \u0905\u0932\u093E\u0935\u093E \u0935\u0948\u0936\u094D\u0935\u093F\u0915 \u0938\u094D\u0924\u0930 \u092A\u0947 ban \u092D\u0940 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",
    "* <strong>Global Bot</strong> - Like Moderator, but makes it clear that this user is a bot": "* <strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 Bot</strong> - Moderator \u091C\u0948\u0938\u093E \u092A\u0930 \u0915\u0947\u0935\u0932 Bots \u0915\u0947 \u0932\u093F\u090F",
    "&amp; <strong>Global Administrator</strong> - They can do anything, like change what this message says and promote users globally": "&amp; <strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 Administrator</strong> - \u092F\u0947 \u0932\u094B\u0917 \u0915\u0941\u091B \u092D\u0940 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902, \u091C\u0948\u0938\u0947 \u0915\u0940 \u0907\u0938 \u0938\u0928\u094D\u0926\u0947\u0936 \u0915\u094B \u092C\u0926\u0932\u0928\u093E",
    "<strong>Room ranks</strong>": "<strong>\u0930\u0942\u092E \u0915\u0947 \u092A\u0926</strong>",
    "^ <strong>Prize Winner</strong> - They don't have any powers beyond a symbol.": "",
    "+ <strong>Voice</strong> - They can use ! commands like !groups": "+ <strong>Voice</strong> - \u092F\u0947 \u0932\u094B\u0917 '!' commands \u0915\u093E \u0907\u0938\u094D\u0924\u0947\u092E\u093E\u0932 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902, \u091C\u0948\u0938\u0947 \u0915\u0940 !groups",
    "% <strong>Driver</strong> - The above, and they can mute and warn": "% <strong>Driver</strong> - \u092F\u0947 \u0932\u094B\u0917 \u090A\u092A\u0930 \u0915\u0940 \u091A\u0940\u091C\u093C\u0947\u0902 \u0914\u0930 \u0909\u0938\u0915\u0947 \u0905\u0932\u093E\u0935\u093E mute \u0914\u0930 warn \u092D\u0940 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",
    "@ <strong>Moderator</strong> - The above, and they can room ban users": "@ <strong>Moderator</strong> - \u092F\u0947 \u0932\u094B\u0917 \u090A\u092A\u0930 \u0915\u0940 \u091A\u0940\u091C\u093C\u0947\u0902 \u0914\u0930 \u0909\u0938\u0915\u0947 \u0905\u0932\u093E\u0935\u093E room ban \u092D\u0940 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",
    "* <strong>Bot</strong> - Like Moderator, but makes it clear that this user is a bot": "* <strong>Bot</strong> - Moderator \u091C\u0948\u0938\u093E \u092A\u0930 \u0915\u0947\u0935\u0932 Bots \u0915\u0947 \u0932\u093F\u090F",
    "# <strong>Room Owner</strong> - They are leaders of the room and can almost totally control it": "# <strong>Room Owner</strong> - \u092F\u0947 \u0932\u094B\u0917 room \u0915\u0947 leader \u0939\u0948\u0902 \u0914\u0930 \u0930\u0942\u092E \u0932\u0917\u092D\u0917 \u092A\u0942\u0930\u0940 \u0924\u0930\u0939 \u0907\u0928\u0915\u0947 \u0905\u0927\u0940\u0928 \u0939\u0948",
    "/help OR /h OR /? - Gives you help.": "/help \u092F\u093E /h \u092F\u093E /? - \u0906\u092A\u0915\u094B \u0938\u0939\u093E\u092F\u0924\u093E \u0926\u0947.",
    "For an overview of room commands, use /roomhelp": "Room \u0915\u0947 \u0915\u092E\u093E\u0902\u0921\u094D\u0938 \u0915\u0947 \u0938\u093E\u0930\u093E\u0902\u0936 \u0915\u0947 \u0932\u093F\u090F, /roomhelp \u0909\u092A\u092F\u094B\u0917 \u0915\u0930\u0947\u0902",
    "For details of a specific command, use something like: /help data": "\u0915\u093F\u0938\u0940 \u0916\u093E\u0938 \u0915\u092E\u093E\u0902\u0921 \u0915\u0947 \u0935\u093F\u0935\u0930\u0923 \u0915\u0947 \u0932\u093F\u090F, \u0915\u0941\u091B \u0910\u0938\u0947 \u0915\u0930\u0947\u0902: /help data",
    "COMMANDS": "\u0915\u092E\u093E\u0902\u0921",
    "BATTLE ROOM COMMANDS": "\u092E\u0941\u0915\u093E\u092C\u0932\u0947 \u0915\u0947 \u0915\u092E\u093E\u0902\u0921",
    "OPTION COMMANDS": "\u0935\u093F\u0915\u0932\u094D\u092A\u094B\u0902 \u0915\u0947 \u0915\u092E\u093E\u0902\u0921",
    "INFORMATIONAL/RESOURCE COMMANDS": "\u0938\u0942\u091A\u0928\u093E\u0924\u094D\u092E\u0915/\u0938\u0902\u0938\u093E\u0927\u0928 \u0938\u0902\u092C\u0902\u0927\u0940 \u0915\u092E\u093E\u0902\u0921",
    "DATA COMMANDS": "\u0921\u0947\u091F\u093E \u0938\u0902\u092C\u0902\u0927\u0940 \u0915\u092E\u093E\u0902\u0921",
    "DRIVER COMMANDS": "Drivers \u0915\u0947 \u0915\u092E\u093E\u0902\u0921",
    "MODERATOR COMMANDS": "Moderators \u0915\u0947 \u0915\u092E\u093E\u0902\u0921",
    "ADMIN COMMANDS": "Administrators \u0915\u0947 \u0915\u092E\u093E\u0902\u0921",
    "(replace / with ! to broadcast. Broadcasting requires: + % @ # &)": "(\u092A\u094D\u0930\u0938\u093E\u0930\u093F\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F / \u0915\u094B ! \u0938\u0947 \u092C\u0926\u0932\u0947\u0902. \u092A\u094D\u0930\u0938\u093E\u0930\u0923 \u0915\u0947 \u0932\u093F\u090F \u0906\u0935\u0936\u094D\u092F\u0915 \u092A\u0926: + % @ # &) ",
    "<strong>Room punishments</strong>:": "<strong>Room \u0915\u0947 \u0926\u0902\u0921</strong>:",
    "<strong>warn</strong> - Displays a popup with the rules.": "<strong>warn</strong> - \u0928\u093F\u092F\u092E\u094B\u0902 \u0915\u093E \u090F\u0915 popup \u0926\u093F\u0916\u093E\u0924\u093E \u0939\u0948.",
    "<strong>mute</strong> - Mutes a user (makes them unable to talk) for 7 minutes.": "<strong>mute</strong> - 7 \u092E\u093F\u0928\u091F\u094B\u0902 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u091A\u0941\u092A (\u092C\u093E\u0924\u091A\u0940\u0924 \u092E\u0947\u0902 \u0905\u0938\u092E\u0930\u094D\u0925) \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>hourmute</strong> - Mutes a user for 60 minutes.": "<strong>hourmute</strong> - 60 \u092E\u093F\u0928\u091F\u094B\u0902 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u091A\u0941\u092A \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>ban</strong> - Bans a user (makes them unable to join the room) for 2 days.": "<strong>ban</strong> - 2 \u0926\u093F\u0928 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u0928\u093F\u0937\u094D\u0915\u093E\u0938\u093F\u0924 (room \u0938\u0947 \u091C\u0941\u095C\u0928\u0947 \u092E\u0947\u0902 \u0905\u0938\u092E\u0930\u094D\u0925) \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>weekban</strong> - Bans a user from the room for a week.": "<strong>weekban</strong> - \u090F\u0915 \u0938\u092A\u094D\u0924\u093E\u0939 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u0928\u093F\u0937\u094D\u0915\u093E\u0938\u093F\u0924 (room \u0938\u0947 \u091C\u0941\u095C\u0928\u0947 \u092E\u0947\u0902 \u0905\u0938\u092E\u0930\u094D\u0925) \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>blacklist</strong> - Bans a user for a year.": "<strong>blacklist</strong> - \u0938\u093E\u0932 \u092D\u0930 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u0928\u093F\u0937\u094D\u0915\u093E\u0938\u093F\u0924 \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>Global punishments</strong>:": "<strong>\u0935\u0948\u0936\u094D\u0935\u093F\u0915 \u0926\u0902\u0921</strong>:",
    "<strong>lock</strong> - Locks a user (makes them unable to talk in any rooms or PM non-staff) for 2 days.": "<strong>lock</strong> - 2 \u0926\u093F\u0928 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B lock (rooms \u0914\u0930 \u0917\u0948\u0930-\u0938\u094D\u091F\u093E\u092B \u0915\u0947 PMs \u092E\u0947\u0902 \u092C\u093E\u0924\u091A\u0940\u0924 \u092E\u0947\u0902 \u0905\u0938\u092E\u0930\u094D\u0925) \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>weeklock</strong> - Locks a user for a week.": "<strong>weeklock</strong> - \u090F\u0915 \u0938\u092A\u094D\u0924\u093E\u0939 \u0915\u0947 \u0932\u093F\u090F \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B lock \u0915\u0930\u0924\u093E \u0939\u0948.",
    "<strong>namelock</strong> - Locks a user and prevents them from having a username for 2 days.": "<strong>namelock</strong> - \u0909\u092A\u092D\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u0932\u0949\u0915 \u0915\u0930\u0947 \u0914\u0930 2 \u0926\u093F\u0928 \u0915\u0947 \u0932\u093F\u090F \u0935\u094B \u0928\u093E\u092E \u0930\u0916\u0928\u0947 \u0938\u0947 \u0930\u094B\u0915\u0924\u093E \u0939\u0948.",
    "<strong>globalban</strong> - Globally bans (makes them unable to connect and play games) for a week.": "<strong>globalban</strong> - \u090F\u0915 \u0938\u092A\u094D\u0924\u093E\u0939 \u0915\u0947 \u0932\u093F\u090F \u0935\u0948\u0936\u094D\u0935\u093F\u0915 \u0924\u094C\u0930 \u092A\u0947 \u0928\u093F\u0937\u094D\u0915\u093E\u0938\u093F\u0924 \u0915\u0930\u0924\u093E (connect \u0914\u0930 \u0916\u0947\u0932\u0928\u0947 \u0939\u094B\u0928\u0947 \u0938\u0947 \u0930\u094B\u0915\u0924\u093E) \u0939\u0948.",
    "<strong>Indefinite global punishments</strong>:": "<strong>\u0905\u0928\u093F\u0936\u094D\u091A\u093F\u0924\u0915\u093E\u0932\u0940\u0928 \u0935\u0948\u0936\u094D\u0935\u093F\u0915 \u0926\u0902\u0921</strong>:",
    "<strong>permalock</strong> - Issued for repeated instances of bad behavior and is rarely the result of a single action. ": "<strong>permalock</strong> - \u0932\u0917\u093E\u0924\u093E\u0930 \u092C\u0941\u0930\u0947 \u0935\u094D\u092F\u0935\u0939\u093E\u0930 \u0915\u0947 \u0932\u093F\u090F \u092E\u093F\u0932\u0928\u0947 \u0935\u093E\u0932\u093E \u0926\u0902\u0921. \u0924\u0940\u0928 \u092E\u093E\u0939 \u0924\u0915 \u0915\u093F\u0938\u0940 \u092D\u0940 \u0926\u0941\u0930\u094D\u0935\u094D\u092F\u0935\u0939\u093E\u0930 \u0938\u0947 \u0926\u0942\u0930 \u0930\u0939\u0928\u0947 \u0915\u0947 \u092C\u093E\u0926 \u0939\u0940 \u0907\u0938\u0947 ",
    'These can be appealed in the <a href="https://www.smogon.com/forums/threads/discipline-appeal-rules.3583479/">Discipline Appeal</a>': '<a href="https://www.smogon.com/forums/threads/discipline-appeal-rules.3583479/">Discipline Appeal</a> forum \u092A\u0930 \u0905\u092A\u0940\u0932 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902.',
    " forum after at least 3 months without incident.": "",
    "<strong>permaban</strong> - Unappealable global ban typically issued for the most severe cases of offensive/inappropriate behavior.": "<strong>permaban</strong> - \u0938\u092C\u0938\u0947 \u0917\u0902\u092D\u0940\u0930 \u092E\u093E\u092E\u0932\u094B\u0902 \u0915\u0947 \u0932\u093F\u090F \u092E\u093F\u0932\u093E \u0939\u0941\u0906 \u0938\u094D\u0925\u093E\u0908 \u0928\u093F\u0937\u094D\u0915\u093E\u0936\u0928. \u092F\u0947 \u0926\u0902\u0921 \u0905\u092A\u0940\u0932 \u0915\u0947 \u0932\u093F\u090F \u0905\u092F\u094B\u0917\u094D\u092F \u0939\u0948.",
    "<strong>Room drivers (%)</strong> can use:": "<strong>Room driver (%)</strong> \u0909\u092A\u092F\u094B\u0917 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902:",
    "- /warn OR /k <em>username</em>: warn a user and show the Pok&eacute;mon Showdown rules": "- /warn \u092F\u093E /k <em>username</em>: \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u091A\u0947\u0924\u093E\u0935\u0928\u0940 \u0926\u0947 \u0914\u0930 Pok&eacute;mon Showdown \u0915\u0947 \u0928\u093F\u092F\u092E \u0926\u093F\u0916\u093E\u090F",
    "- /mute OR /m <em>username</em>: 7 minute mute": "- /mute \u092F\u093E /m <em>username</em>: 7 \u092E\u093F\u0928\u091F \u0915\u093E mute",
    "- /hourmute OR /hm <em>username</em>: 60 minute mute": "- /hourmute \u092F\u093E /hm <em>username</em>: 60 \u092E\u093F\u0928\u091F \u0915\u093E mute",
    "- /unmute <em>username</em>: unmute": "- /unmute <em>username</em>: mute \u0939\u091F\u093E\u090F",
    "- /hidetext <em>username</em>: hide a user's messages from the room": "- /hidetext <em>username</em>: room \u092E\u0947\u0902 \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u0947 \u0938\u0928\u094D\u0926\u0947\u0936 \u091B\u0941\u092A\u093E\u092F\u0947",
    "- /announce OR /wall <em>message</em>: make an announcement": "- /announce \u092F\u093E /wall <em>\u0938\u0928\u094D\u0926\u0947\u0936</em>: \u0918\u094B\u0937\u0923\u093E \u0915\u0930\u0947",
    "- /modlog <em>username</em>: search the moderator log of the room": "- /modlog <em>username</em>: room \u0915\u0947 moderator log \u092E\u0947\u0902 \u0916\u094B\u091C\u0947",
    "- /modnote <em>note</em>: add a moderator note that can be read through modlog": "- /modnote <em>\u091F\u093F\u092A\u094D\u092A\u0923\u0940</em>: \u090F\u0915 moderator \u091F\u093F\u092A\u094D\u092A\u0923\u0940 \u0921\u093E\u0932\u0947 \u091C\u094B \u0915\u0940 modlog \u092E\u0947\u0902 \u092A\u095D\u0940 \u091C\u093E \u0938\u0915\u0924\u0940 \u0939\u0948",
    "<strong>Room moderators (@)</strong> can also use:": "<strong>Room moderator (@)</strong> \u0907\u0928\u0915\u093E \u092D\u0940 \u0909\u092A\u092F\u094B\u0917 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902:",
    "- /roomban OR /rb <em>username</em>: ban user from the room": "- /roomban \u092F\u093E /rb <em>username</em>: \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B room \u0938\u0947 \u0928\u093F\u0937\u094D\u0915\u093E\u0938\u093F\u0924 \u0915\u0930\u0947",
    "- /roomunban <em>username</em>: unban user from the room": "- /roomunban <em>username</em>: \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B room \u092E\u0947\u0902 \u0905\u0928\u093F\u0937\u094D\u0915\u093E\u0938\u093F\u0924 \u0915\u0930\u0947",
    "- /roomvoice <em>username</em>: appoint a room voice": "- /roomvoice <em>username</em>: room voice \u0928\u093F\u092F\u0941\u0915\u094D\u0924 \u0915\u0930\u0947",
    "- /roomdevoice <em>username</em>: remove a room voice": "- /roomdevoice <em>username</em>: room voice \u0939\u091F\u093E\u090F",
    "- /staffintro <em>intro</em>: set the staff introduction that will be displayed for all staff joining the room": "- /staffintro <em>intro</em>: staff \u0915\u0947 \u0932\u093F\u090F \u092A\u0930\u093F\u091A\u092F \u0938\u0928\u094D\u0926\u0947\u0936 \u0930\u0916\u0947, \u091C\u094B \u0915\u0940 \u0939\u0930 \u091C\u0941\u095C\u0928\u0947 \u0935\u093E\u0932\u0947 staff \u0915\u094B \u0926\u093F\u0916\u0947\u0917\u093E.",
    "- /roomsettings: change a variety of room settings, namely modchat": "- /roomsettings: room \u0915\u0947 \u0935\u093F\u0935\u093F\u0927 \u0938\u0947\u091F\u093F\u0902\u0917 \u092C\u0926\u0932\u0947, \u092F\u093E\u0928\u0940 modchat.",
    "<strong>Room owners (#)</strong> can also use:": "<strong>Room owners (#)</strong> \u0907\u0928\u0915\u093E \u092D\u0940 \u0909\u092A\u092F\u094B\u0917 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902:",
    "- /roomintro <em>intro</em>: set the room introduction that will be displayed for all users joining the room": "- /roomintro <em>intro</em>: room \u0915\u0947 \u0932\u093F\u090F \u092A\u0930\u093F\u091A\u092F \u0938\u0928\u094D\u0926\u0947\u0936 \u0930\u0916\u0947, \u091C\u094B \u0915\u0940 \u0939\u0930 \u091C\u0941\u095C\u0928\u0947 \u0935\u093E\u0932\u0947 \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u0926\u093F\u0916\u0947\u0917\u093E.",
    "- /rules <em>rules link</em>: set the room rules link seen when using /rules": "- /rules <em>\u0928\u093F\u092F\u092E\u094B\u0902 \u0915\u093E \u0932\u093F\u0902\u0915</em>: room \u0915\u0947 \u0928\u093F\u092F\u092E\u094B\u0902 \u0915\u093E \u0932\u093F\u0902\u0915 \u0930\u0916\u0947 \u091C\u094B \u0915\u0940 /rules \u0938\u0947 \u0926\u0947\u0916\u093E \u091C\u093E \u0938\u0915\u0924\u093E \u0939\u0948",
    "- /roommod, /roomdriver <em>username</em>: appoint a room moderator/driver": "- /roommod, /roomdriver <em>username</em>: room moderador/driver \u0928\u093F\u092F\u0941\u0915\u094D\u0924 \u0915\u0930\u0947",
    "- /roomdemod, /roomdedriver <em>username</em>: remove a room moderator/driver": "- /roomdemod, /roomdedriver <em>username</em>: room moderador/driver \u0939\u091F\u093E\u090F",
    "- /roomdeauth <em>username</em>: remove all room auth from a user": "- /roomdeauth <em>username</em>: \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B room \u0915\u0947 \u0938\u092D\u0940 \u092A\u0926\u094B\u0902 \u0938\u0947 \u0939\u091F\u093E\u090F",
    "- /declare <em>message</em>: make a large blue declaration to the room": "- /declare <em>\u0938\u0928\u094D\u0926\u0947\u0936</em>: room \u092E\u0947\u0902 \u090F\u0915 \u092C\u095C\u093E \u0928\u0940\u0932\u093E \u0910\u0932\u093E\u0928 \u0915\u0930\u0947",
    "- !htmlbox <em>HTML code</em>: broadcast a box of HTML code to the room": "- !htmlbox <em>HTML code</em>: room \u092E\u0947\u0902 HTML code \u0915\u0947 \u090F\u0915 \u0921\u092C\u094D\u092C\u0947 \u0915\u094B \u092A\u094D\u0930\u0938\u093E\u0930\u093F\u0924 \u0915\u0930\u0947",
    "- !showimage <em>[url], [width], [height]</em>: show an image to the room": "- !showimage <em>[url], [width], [height]</em>: room \u092E\u0947\u0902 \u090F\u0915 \u091A\u093F\u0924\u094D\u0930 \u092A\u094D\u0930\u0926\u0930\u094D\u0936\u093F\u0924 \u0915\u0930\u0947",
    "- /roomsettings: change a variety of room settings, including modchat, capsfilter, etc": "- /roomsettings: room \u0915\u0947 \u0935\u093F\u0935\u093F\u0927 \u0938\u0947\u091F\u093F\u0902\u0917 \u092C\u0926\u0932\u0947, \u091C\u0948\u0938\u0947 \u0915\u0940  modchat, capsfilter \u0906\u0926\u093F",
    'More detailed help can be found in the <a href="https://www.smogon.com/forums/posts/6774654/">roomauth guide</a>': '\u0914\u0930 \u091C\u094D\u092F\u093E\u0926\u093E \u0935\u093F\u0938\u094D\u0924\u0943\u0924 \u0938\u0939\u093E\u092F\u0924\u093E <a href="https://www.smogon.com/forums/posts/6774654/">roomauth guide</a> \u092E\u0947\u0902 \u092E\u093F\u0932 \u0938\u0915\u0924\u0940 \u0939\u0948',
    "Tournament Help:": "Tournament \u0938\u0947 \u091C\u0941\u095C\u0940 \u0938\u0939\u093E\u092F\u0924\u093E:",
    "- /tour create <em>format</em>, elimination: create a new single elimination tournament in the current room.": "- /tour create <em>\u092A\u094D\u0930\u093E\u0930\u0942\u092A</em>, elimination: room \u092E\u0947\u0902 \u090F\u0915 \u0928\u092F\u093E \u0938\u093F\u0902\u0917\u0932 \u090F\u0932\u093F\u092E\u093F\u0928\u0947\u0936\u0928 \u091F\u0942\u0930 \u092C\u0928\u093E\u092F\u0947.",
    "- /tour create <em>format</em>, roundrobin: create a new round robin tournament in the current room.": "- /tour create <em>\u092A\u094D\u0930\u093E\u0930\u0942\u092A</em>, roundrobin: room \u092E\u0947\u0902 \u090F\u0915 \u0928\u092F\u093E round robin \u091F\u0942\u0930 \u092C\u0928\u093E\u092F\u0947.",
    "- /tour end: forcibly end the tournament in the current room": "- /tour end: room \u092E\u0947\u0902 \u091C\u092C\u0930\u0926\u0938\u094D\u0924\u0940 \u091F\u0942\u0930 \u0959\u0924\u094D\u092E \u0915\u0930\u0947",
    "- /tour start: start the tournament in the current room": "- /tour start: room \u092E\u0947\u0902 \u091F\u0942\u0930 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947",
    "- /tour banlist [pokemon], [talent], [...]: ban moves, abilities, Pok\xE9mon or items from being used in a tournament (it must be created first)": "- /tour banlist [pokemon], [talent], [...]: \u091F\u0942\u0930 \u0915\u0947 \u0932\u093F\u090F \u0939\u092E\u0932\u0947, ability, Pok\xE9mon, \u092F\u093E \u0938\u093E\u092E\u093E\u0928 \u092A\u094D\u0930\u0924\u093F\u092C\u0902\u0927\u093F\u0924 \u0915\u0930\u0947 (\u091F\u0942\u0930 \u092A\u0939\u0932\u0947 \u092C\u0928\u093E \u0939\u094B\u0928\u093E \u091A\u093E\u0939\u093F\u090F)",
    'More detailed help can be found in the <a href="https://www.smogon.com/forums/posts/6777489/">tournaments guide</a>': '\u0914\u0930 \u091C\u094D\u092F\u093E\u0926\u093E \u0935\u093F\u0938\u094D\u0924\u0943\u0924 \u0938\u0939\u093E\u092F\u0924\u093E <a href="https://www.smogon.com/forums/posts/6777489/">tournaments guide</a> \u092E\u0947\u0902 \u092E\u093F\u0932 \u0938\u0915\u0924\u0940 \u0939\u0948',
    "Your status cannot be updated while you are locked or semilocked.": "\u091C\u092C \u0906\u092A lock \u092F\u093E semilock \u0939\u094B\u0902 \u0924\u092C \u0906\u092A status \u0928\u0939\u0940\u0902 \u092C\u0926\u0932 \u0938\u0915\u0924\u0947.",
    "Your status is too long; it must be under ${maxLength} characters.": "\u0906\u092A\u0915\u093E status \u092C\u0939\u0941\u0924 \u092C\u095C\u093E \u0939\u0948; \u092F\u0947 \u0905\u0927\u093F\u0915\u0924\u092E ${maxLength} \u0905\u0915\u094D\u0937\u0930 \u0915\u093E \u0939\u094B \u0938\u0915\u0924\u093E \u0939\u0948.",
    "Your status contains a banned word.": "\u0906\u092A\u0915\u0947 status \u092E\u0947\u0902 \u090F\u0915 \u092A\u094D\u0930\u0924\u093F\u092C\u0902\u0927\u093F\u0924 \u0936\u092C\u094D\u0926 \u0939\u0948.",
    "Your status has been set to: ${target}.": "\u0906\u092A\u0915\u093E status \u0905\u092C \u092F\u0947 \u0939\u0948 : ${target}.",
    "You are now marked as busy.": "\u0906\u092A\u0915\u094B \u0905\u092C busy (\u0935\u094D\u092F\u0938\u094D\u0924) \u092E\u093E\u0930\u094D\u0915 \u0915\u0930 \u0926\u093F\u092F\u093E \u0917\u092F\u093E \u0939\u0948.",
    "You are now marked as away. Send a message or use /back to indicate you are back.": "\u0906\u092A\u0915\u094B away (\u0926\u0942\u0930) \u092E\u093E\u0930\u094D\u0915 \u0915\u0930 \u0926\u093F\u092F\u093E \u0917\u092F\u093E \u0939\u0948. \u0905\u092A\u0928\u0940 \u0935\u093E\u092A\u0938\u0940 \u0926\u0930\u094D\u0936\u093E\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F \u090F\u0915 \u0938\u0928\u094D\u0926\u0947\u0936 \u092D\u0947\u091C\u0947\u0902 \u092F\u093E /back \u0915\u093E \u0909\u092A\u092F\u094B\u0917 \u0915\u0930\u0947\u0902.",
    "You are already marked as back.": "\u0906\u092A \u092A\u0939\u0932\u0947 \u0938\u0947 \u0939\u0940 (back) \u092E\u0941\u0915\u094D\u0924 \u091A\u093F\u0939\u094D\u0928\u093F\u0924 \u0939\u0948\u0902.",
    "You are no longer marked as busy.": "\u0905\u092C \u0906\u092A (busy) \u0935\u094D\u092F\u0938\u094D\u0924 \u091A\u093F\u0928\u094D\u0939\u093F\u0924 \u0928\u0939\u0940\u0902 \u0939\u0948\u0902.",
    "You must choose a name before you can talk.": "\u092C\u093E\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F \u090F\u0915 \u0928\u093E\u092E \u091A\u0941\u0928\u0947\u0902.",
    "You are ${lockType} and can't talk in chat. ${lockExpiration}": "\u0906\u092A ${lockType} \u0939\u0948\u0902 \u0914\u0930 \u092C\u093E\u0924 \u0928\u0939\u0940\u0902 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902. ${lockExpiration}",
    "Get help with [TN: your lock]this": "\u0907\u0938\u0915\u0947 \u0932\u093F\u090F \u0938\u0939\u093E\u092F\u0924\u093E",
    "You are muted and cannot talk in this room.": "\u0906\u092A \u0907\u0938 room \u092E\u0947\u0902 muted \u0939\u0948\u0902 \u0914\u0930 \u092C\u093E\u0924\u091A\u0940\u0924 \u0928\u0939\u0940 \u0915\u0930 \u0938\u0915\u0924\u0947",
    "Because moderated chat is set, your account must be at least one week old and you must have won at least one ladder game to speak in this room.": "\u0915\u094D\u092F\u094B\u0902\u0915\u093F chat \u0938\u092F\u0902\u092E\u093F\u0924 \u0939\u0948, \u092C\u093E\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F \u0906\u092A\u0915\u093E \u0916\u093E\u0924\u093E \u0915\u092E \u0938\u0947 \u0915\u092E \u090F\u0915 \u0938\u092A\u094D\u0924\u093E\u0939 \u092A\u0941\u0930\u093E\u0928\u093E \u0914\u0930 \u0915\u092E \u0938\u0947 \u0915\u092E \u090F\u0915 \u092E\u0941\u0915\u093E\u092C\u0932\u0947 \u0915\u093E \u0935\u093F\u091C\u0947\u0924\u093E \u0939\u094B\u0928\u093E \u091A\u093E\u0939\u093F\u090F.",
    "Because moderated chat is set, your account must be staff in a public room or have a global rank to speak in this room.": "\u0915\u094D\u092F\u094B\u0902\u0915\u093F chat \u0938\u092F\u0902\u092E\u093F\u0924 \u0939\u0948, \u092C\u093E\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F \u0906\u092A\u0915\u093E \u0916\u093E\u0924\u093E \u0935\u0948\u0936\u094D\u0935\u093F\u0915 \u092A\u0926 \u092F\u093E \u0938\u093E\u0930\u094D\u0935\u091C\u0928\u093F\u0915 room \u092E\u0947\u0902 staff \u0939\u094B\u0928\u093E \u091A\u093E\u0939\u093F\u090F.",
    "Because moderated chat is set, you must be of rank ${groupName} or higher to speak in this room.": "\u0915\u094D\u092F\u094B\u0902\u0915\u093F chat \u0938\u092F\u0902\u092E\u093F\u0924 \u0939\u0948, \u092C\u093E\u0924 \u0915\u0930\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F \u0906\u092A\u0915\u093E \u092A\u0926 ${groupName} \u092F\u093E \u0909\u0938\u0938\u0947 \u090A\u0901\u091A\u093E \u0939\u094B\u0928\u093E \u091A\u093E\u0939\u093F\u090F.",
    "Your message can't be blank.": "\u0906\u092A\u0915\u093E \u0938\u0928\u094D\u0926\u0947\u0936 \u0916\u093E\u0932\u0940 \u0928\u0939\u0940\u0902 \u0939\u094B\u0928\u093E \u091A\u093E\u0939\u093F\u090F.",
    "Your message is too long: ": "\u0906\u092A\u0915\u093E \u0938\u0928\u094D\u0926\u0947\u0936 \u092C\u0939\u0941\u0924 \u0932\u092E\u094D\u092C\u093E \u0939\u0948.",
    "Your message contains banned characters.": "\u0906\u092A\u0915\u0947 \u0938\u0928\u094D\u0926\u0947\u0936 \u092E\u0947\u0902 \u092A\u094D\u0930\u0924\u093F\u092C\u0902\u0927\u093F\u0924 \u0905\u0915\u094D\u0937\u0930 \u0939\u0948\u0902.",
    "This room has slow-chat enabled. You can only talk once every ${time} seconds.": "\u0907\u0938 room \u092E\u0947\u0902 slow-chat \u091A\u093E\u0932\u0942 \u0939\u0948. \u0906\u092A \u0915\u0947\u0935\u0932 \u0939\u0930 ${time} seconds \u092A\u0930 \u092C\u093E\u0924 \u0915\u0930 \u0938\u0915\u0924\u0947 \u0939\u0948\u0902",
    "Your username contains a phrase banned by this room.": "\u0906\u092A\u0915\u0947 \u0928\u093E\u092E \u092E\u0947\u0902 \u0907\u0938 room \u0915\u093E \u090F\u0915 \u092A\u094D\u0930\u0924\u093F\u092C\u0902\u0927\u093F\u0924 \u0936\u092C\u094D\u0926 \u0939\u0948.",
    "Your status message contains a phrase banned by this room.": "\u0906\u092A\u0915\u0947 status \u092E\u0947\u0902 \u0907\u0938 room \u0915\u093E \u090F\u0915 \u092A\u094D\u0930\u0924\u093F\u092C\u0902\u0927\u093F\u0924 \u0936\u092C\u094D\u0926 \u0939\u0948.",
    "You are ${lockType} and can only private message members of the global moderation team. ${lockExpiration}": "",
    "Get help with this": "",
    'The user "${targetUser.name}" is locked and cannot be PMed.': "",
    "On this server, you must be of rank ${groupName} or higher to PM users.": "",
    "This user is blocking private messages right now.": "",
    "This ${Config.groups[targetUser.group].name} is too busy to answer private messages right now. Please contact a different staff member.": "",
    'If you need help, try opening a <a href="view-help-request" class="button">help ticket</a>': "",
    "You are blocking private messages right now.": "",
    "You are blocking challenges right now.": "",
    "Your message contained banned words in this room.": "\u0906\u092A\u0915\u0947 \u0938\u0928\u094D\u0926\u0947\u0936 \u092E\u0947\u0902 \u0907\u0938 room \u0915\u093E \u090F\u0915 \u092A\u094D\u0930\u0924\u093F\u092C\u0902\u0927\u093F\u0924 \u0936\u092C\u094D\u0926 \u0939\u0948.",
    "You can't send the same message again so soon.": "\u0906\u092A \u090F\u0915 \u0939\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0907\u0924\u0928\u0940 \u091C\u0932\u094D\u0926\u0940 \u0926\u094B\u092C\u093E\u0930\u093E \u0928\u0939\u0940\u0902 \u092D\u0947\u091C \u0938\u0915\u0924\u0947.",
    "Due to this room being a high traffic room, your message must contain at least two letters.": "\u0915\u094D\u092F\u094B\u0902\u0915\u093F \u092F\u0947 \u090F\u0915 \u0924\u0940\u0935\u094D\u0930 \u0917\u0924\u093F\u0935\u093F\u0927\u093F \u0935\u093E\u0932\u093E room \u0939\u0948, \u0906\u092A\u0915\u0947 \u0938\u0928\u094D\u0926\u0947\u0936 \u092E\u0947\u0902 \u0915\u092E \u0938\u0947 \u0915\u092E \u0926\u094B \u0905\u0915\u094D\u0937\u0930 \u0930\u0939\u0928\u0947 \u091C\u0930\u0942\u0930\u0940 \u0939\u0948\u0902.",
    "You are already blocking private messages! To unblock, use /unblockpms": "\u0906\u092A \u092A\u0939\u0932\u0947 \u0938\u0947 \u0939\u0940 \u0928\u093F\u091C\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902! \u0916\u094B\u0932\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F /unblockpms \u0909\u092A\u092F\u094B\u0917 \u0915\u0930\u0947\u0902.",
    "You are now blocking private messages, except from staff and ${rank}.": "\u0905\u092C \u0906\u092A staff \u0914\u0930 ${rank} \u0915\u094B \u091B\u094B\u0921\u093C \u0915\u0930 \u0938\u092C\u0915\u0947 \u0932\u093F\u090F \u0928\u093F\u091C\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902.",
    "You are now blocking private messages, except from staff and ${status} users.": "\u0905\u092C \u0906\u092A staff \u0914\u0930 ${status} \u0909\u092A\u092F\u094B\u0917\u0915\u0930\u094D\u0924\u093E \u0915\u094B \u091B\u094B\u0921\u093C \u0915\u0930 \u0938\u092C\u0915\u0947 \u0932\u093F\u090F \u0928\u093F\u091C\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902.",
    "You are now blocking private messages, except from staff.": "\u0905\u092C \u0906\u092A staff \u0915\u094B \u091B\u094B\u0921\u093C \u0915\u0930 \u0938\u092C\u0915\u0947 \u0932\u093F\u090F \u0928\u093F\u091C\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902.",
    "You are not blocking private messages! To block, use /blockpms": "\u0906\u092A \u0928\u093F\u091C\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0928\u0939\u0940\u0902 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902! \u0930\u094B\u0915\u0928\u0947 \u0915\u0947 \u0932\u093F\u090F /blockpms \u0915\u093E \u0909\u092A\u092F\u094B\u0917 \u0915\u0930\u0947\u0902.",
    "You are no longer blocking private messages.": "\u0905\u092C \u0906\u092A \u0928\u093F\u091C\u0940 \u0938\u0928\u094D\u0926\u0947\u0936 \u0928\u0939\u0940\u0902 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902.",
    "You are now blocking all incoming challenge requests.": "\u0906\u092A \u0905\u092C \u0938\u092D\u0940 \u092E\u0941\u0915\u093E\u092C\u0932\u0947 \u0915\u0947 \u0905\u0928\u0941\u0930\u094B\u0927 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902.",
    "You are already blocking challenges!": " \u0906\u092A \u092A\u0939\u0932\u0947 \u0938\u0947 \u0939\u0940 \u092E\u0941\u0915\u093E\u092C\u0932\u0947 \u0930\u094B\u0915 \u0930\u0939\u0947 \u0939\u0948\u0902!",
    "You are already available for challenges!": "\u0906\u092A \u092A\u0939\u0932\u0947 \u0938\u0947 \u0939\u0940 \u092E\u0941\u0915\u093E\u092C\u0932\u0947 \u0915\u0947 \u0932\u093F\u090F \u0924\u0948\u092F\u093E\u0930 \u0939\u0948\u0902!",
    "You are available for challenges from now on.": "\u0905\u092C \u0906\u092A \u092E\u0941\u0915\u093E\u092C\u0932\u094B\u0902 \u0915\u0947 \u0932\u093F\u090F \u0924\u0948\u092F\u093E\u0930 \u0939\u0948\u0902.",
    "You are now blocking challenges, except from staff and ${rank}.": "",
    "You are now blocking challenges, except from staff and ${status} users.": "",
    "Staff FAQ": "",
    "You cannot broadcast all FAQs at once.": "",
    "A user is autoconfirmed when they have won at least one rated battle and have been registered for one week or longer. In order to prevent spamming and trolling, most chatrooms only allow autoconfirmed users to chat. If you are not autoconfirmed, you can politely PM a staff member (staff have %, @, or # in front of their username) in the room you would like to chat and ask them to disable modchat. However, staff are not obligated to disable modchat.": "",
    "How the ladder works": "",
    "Tiering FAQ": "",
    "Badge FAQ": "",
    "Common misconceptions about our RNG": "",
    "To join a room tournament, click the <strong>Join!</strong> button or type the command <code>/tour join</code> in the room's chat. You can check if your team is legal for the tournament by clicking the <strong>Validate</strong> button once you've joined and selected a team. To battle your opponent in the tournament, click the <strong>Ready!</strong> button when it appears. There are two different types of room tournaments: elimination (if a user loses more than a certain number of times, they are eliminated) and round robin (all users play against each other, and the user with the most wins is the winner).": "",
    "Frequently Asked Questions": "",
    "pages/faq": "pages/faq",
    "pages/ladderhelp": "pages/ladderhelp",
    "pages/rng": "pages/rng",
    "pages/staff": "pages/staff",
    "- We log PMs so you can report them - staff can't look at them without permission unless there's a law enforcement reason.": "",
    "- We log IPs to enforce bans and mutes.": "",
    "- We use cookies to save your login info and teams, and for Google Analytics and AdSense.": "",
    '- For more information, you can read our <a href="https://${Config.routes.root}/privacy">full privacy policy.</a>': ""
  }
};
//# sourceMappingURL=main.js.map