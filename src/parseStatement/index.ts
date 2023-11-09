import xml2js from 'xml2js';
import fs from 'fs/promises';
import { Wages } from '../wage-index';

const NS = 'osss';
const parser = new xml2js.Parser();
const supportedVersion = "http://ssa.gov/osss/schemas/2.0";

async function getWages(fileName: string){
    const data = await fs.readFile(fileName);
    const result = await parser.parseStringPromise( data );
    const schema = result[`${NS}:OnlineSocialSecurityStatementData`]['$'][`xmlns:${NS}`];
    if (schema !== supportedVersion) {
        throw `${schema} is not supported (${supportedVersion})`;
    }
    const results: any[]  = result[`${NS}:OnlineSocialSecurityStatementData`][`${NS}:EarningsRecord`][0][`${NS}:Earnings`];
    const earnings: Wages = results.reduce((acc, earn: any) => (
        acc[earn['$'].startYear] = parseInt(earn[`${NS}:FicaEarnings`][0]), acc ) as Wages
    , {} as Wages);

    return earnings;
}

export default getWages;