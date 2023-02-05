
const calc = require('./lib');
const parse = require('./lib/parseStatement');

const earnings = require('./test-data');
const compound = require('compound-calc');

const earningsFromXml = parse('Your_Social_Security_Statement_Data.xml').then( (val) => {
    console.log('hi');
    console.log(val);
    console.log( calc(val) );
}).catch(err => console.log(err));

const start = 2022;
const years = 22;
const rate = .02;
const missing = (earnings, start, years, rate) =>
    // merges the passed in earnings with the results of compound.reduce()
    ({...earnings, ...compound(Object.values(earnings).at(-1),0,years,rate).result
        .slice(1) // slice off the first result, which is a duplicate of last earnings
        // use reduce to return object which continues the year series
        .reduce((acc, cur, i) => ((acc[start+i] = Math.round(cur)) && acc),{})
    });


const predicted = missing(earnings, start, years, rate);
// console.log(predicted);

const filledIn = {
    '2000': 38915,
    '2001': 40862.15,
    '2002': 42906.74,
    '2003': 45053.62,
    '2004': 47307.93,
    '2005': 49675.03,
    '2006': 52160.58,
    '2007': 54770.49,
    '2008': 57510.99,
    '2009': 60388.61,
    '2010': 63410.22,
    '2011': 66583.02,
    '2012': 69914.57,
    '2013': 73412.82,
    '2014': 77086.12,
    '2015': 80943.2,
    '2016': 84993.28,
    '2017': 89246.01,
    '2018': 93711.54,
    '2019': 98400.49,
    '2020': 103324.07,
    '2021': 108494
  }

const longRangeIntermediate = {
    2035: 102530.83,
    2040: 122417.01,
    2045: 145582.26,
};



const A = 1000;
const P = 500;
const t = 3;
let r = Math.pow((A/P),(1/t))-1
// console.log(compound(P,0,t,r));



// console.log(earnings);
//console.log(calc(filledIn));
// console.log( calc(earnings) );