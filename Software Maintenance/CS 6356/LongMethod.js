class LongMethod {
    allInOne() {
        let count = 0;
        let x = 5;
        let y = 2;
        let perfect = 100;
        let answer = 0;

        if (x === 4 || y === 1) {
            return "You are close.";
        }
        else if (x === 5 && y === 2) {
            count++;
            return "You got the answer. Your streak is: " + count;
        }

        if (answer != perfect) {
            return "try using words this time.";
        }
    }
}

class FixedMethod {
    mainFn() {
        let count = 0;
        let x = 5;
        let y = 2;
        let perfect = 100;
        let answer = 0;

        this.guessNumber(x, y, count);

        this.useWords(answer, perfect);
    }

    guessNumber(x, y, count) {
        if (x === 4 || y === 1) {
            return "You are close.";
        }
        else if (x === 5 && y === 2) {
            count++;
            return "You got the answer. Your streak is: " + count;
        }
    }

    useWords(answer, perfect) {
        if (answer != perfect) {
            return "try using words this time.";
        }
    }
}