import {wageIndex, Wages} from '../wage-index.js';

const YOUTH_FACTOR = 8;
const YOUTH_FACTOR_AGE = 21;
const WORK_START_AGE = 18;
const CURRENT_YEAR_INCREASE = .96;
const CURRENT_YEAR = new Date().getFullYear();

export function getEstimatedEarnings(age: number, lastWage: number, lastYearWorked: number = CURRENT_YEAR, earningGrowthRate: number = 0){
    if (age <= 22) {
        throw new Error('Age must be greater than 22');
    }
    if (lastYearWorked > CURRENT_YEAR) {
        throw new Error('Last year worked cannot be in the future');
    }
    const workStartYear = CURRENT_YEAR - age + WORK_START_AGE;
    const yearTurned22 = CURRENT_YEAR - age + YOUTH_FACTOR_AGE;

    const wageResults: Wages = {};
    for(let i = lastYearWorked; i >= workStartYear; i--){
        const reductionFactor = getReductionFactor(i) / (1 + earningGrowthRate);
        const youthFactor = i === yearTurned22 ? YOUTH_FACTOR : 1;
        if(i === lastYearWorked){
            wageResults[i] = lastWage;
        } else {
            wageResults[i] = (wageResults[i + 1] * reductionFactor)/youthFactor;
        }
    }
    return wageResults;
}

function getReductionFactor(year: number) {
    if (year === CURRENT_YEAR && !wageIndex[year - 1]) {
        throw new Error('Wage index for previous year is required');
    }
    if (year === CURRENT_YEAR) {
        return 1;
    } else if (year === CURRENT_YEAR - 1) {
        return CURRENT_YEAR_INCREASE
    } else {
        return (wageIndex[year] / wageIndex[year+1]);
    }
}

// console.log(getEstimatedEarnings(70, 100000, 2020, .02));