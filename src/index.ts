import {wageIndex, Wages} from './wage-index.js';

export const calc = (earnings: Wages) => {
    const lookbackYears = 35;
    const futureYearsFactor = 1;
    const bendPointDivisor = 9779.44;
    const firstBendPointMultiplier = 180;
    const secondBendPointMultiplier = 1085;
    const averageWageLastYear = Math.max(...Object.keys(wageIndex).map( val => parseInt(val)));
    const firstBendPoint = Math.round(firstBendPointMultiplier * wageIndex[averageWageLastYear] / bendPointDivisor);
    const secondBendPoint = Math.round(secondBendPointMultiplier * wageIndex[averageWageLastYear] / bendPointDivisor);

    // calculate the wage index factors
    const wageIndexFactors: Wages = Object.entries(wageIndex).reduce(( acc, [i, val], ) => (
        (acc[i] = 1 + (wageIndex[averageWageLastYear] - val) / val) && acc ) as Wages
    , {} as Wages);

    // adjust the earnings according to the wage index factor,
    // factor is 1 for any earnings record without a wage-factor
    const adjustedEarnings: Wages = Object.entries(earnings).reduce(( acc, [i, val], ) => (
        (acc[i] = val * (wageIndexFactors[i] || futureYearsFactor)) && acc ) as Wages
    , {} as Wages);

    const top35YearsEarnings = Object.values(adjustedEarnings)
        .sort((a,b) => b - a) // sort the earnings from highest to lowest amount
        .slice(0,lookbackYears) // grab the highest 35 earnings years
        .reduce((partialSum, a) => partialSum + a, 0); // and finally sum them
    const AIME = top35YearsEarnings / (12 * lookbackYears);

    const normalMonthlyBenefit = (()=>{
        let monthlyBenefit = 0;
        if (AIME <= firstBendPoint) {
            monthlyBenefit = 0.9 * AIME;
        } else {
            if (AIME > firstBendPoint && AIME <= secondBendPoint) {
                monthlyBenefit = 0.9 * firstBendPoint + 0.32 * (AIME - firstBendPoint);
            } else {
                monthlyBenefit = 0.9 * firstBendPoint + 0.32 * (secondBendPoint - firstBendPoint) + 0.15 * (AIME - secondBendPoint);
            }
        }
        return Math.floor(monthlyBenefit * 10.0) / 10.0;
    })();

    const reducedMonthlyBenefit = Math.floor(( 0.7 * normalMonthlyBenefit) * 10)/10;
    const results = {
        "Top35YearsEarnings": top35YearsEarnings.toFixed(2),
        "AIME": AIME.toFixed(2),
        "FirstBendPoint": firstBendPoint.toFixed(2),
        "SecondBendPoint": secondBendPoint.toFixed(2),
        "NormalMonthlyBenefit": normalMonthlyBenefit.toFixed(2),
        "NormalAnnualBenefit": (normalMonthlyBenefit * 12).toFixed(2),
        "ReducedMonthlyBenefit": reducedMonthlyBenefit.toFixed(2),
        "ReducedAnnualBenefit": (reducedMonthlyBenefit * 12).toFixed(2),
    }

    return results;
}
