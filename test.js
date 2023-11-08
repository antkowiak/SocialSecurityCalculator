import {calc} from './lib/index.js';
import parse from './lib/parseStatement/index.js';
import { earnings } from './test-data.js';
import { compound } from 'compound-calc';

const earningsFromXml = await parse('social-security-statement-2023.xml');
console.log( calc(earningsFromXml) );

const start = 2023;
const years = 67-(start-1977);
const rate = 0.02;

const missing = (earnings, start, years, rate) =>
    // merges the passed in earnings with the results of compound.reduce()
    ({...earnings, ...compound(Object.values(earnings).at(-1),0,years,rate).result
        .slice(1) // slice off the first result, which is a duplicate of last earnings
        // use reduce to return object which continues the year series
        .reduce((acc, cur, i) => (acc[start+i] = Math.round(cur), acc),{})
    });


const predicted = missing(earningsFromXml, start, years, rate);

console.log(calc(predicted));
