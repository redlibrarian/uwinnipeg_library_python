import * as fs from 'fs';

const test_dir = "../test-data/";
const test_data = [26171, 22586, 6573];

const SUCCESS = 0; // successful logins
const USER = 1; // sorted by user
const FAILURE = 2;  // failures

function sameArray(array1, array2){
	return array1.length === array2.length && array1.every((value, index) => value === array2[index])
}

function status(line){
	return line.split('\t')[1];
}

function pretty_print(proxy_data){
	console.log(`Total successful logins: ${proxy_data[0]}; sorted by users: ${proxy_data[1]}; failures: ${proxy_data[2]}.`);
  }

function processSingleFile(filename){

	let logins: Array<number> = [0, 0, 0]; //successful logins, sorted by user, failures

	const lines = fs.readFileSync(filename, {encoding: 'utf8', flag: 'r'}).split('\n');

	for(var line of lines){
	       switch(status(line)){
		       case "Login.Success": {
				  logins[SUCCESS] += 1;
				   logins[USER] += 1;
			       break;
		       }
		       case "Login.Success.Relogin": {
				   logins[SUCCESS] += 1;
			       break;
		       }
		       case "Login.Failure": {
				    logins[FAILURE] += 1;
			       break;
		       }
	       }
	}
	return logins;
}

function processDirectory(dir){

	let total_logins: Array<number> = [0, 0, 0]; // successful logins, sorted by user, failures

	let filenames = fs.readdirSync(dir);
	
	for(var file of filenames){
		
		let logins = processSingleFile(`${dir}${file}`);
	    
		total_logins[SUCCESS] += logins[SUCCESS];
		total_logins[USER] += logins[USER];
		total_logins[FAILURE] += logins[FAILURE];
	
	}
	return total_logins;
}

function runTest(){
	console.log("Running test...")
	let test_run = processDirectory(test_dir)
	if(sameArray(test_run, test_data)){
		console.log("%c Test passed.", "color:green");
	} else {
		console.log("%c Test failed.", "color:red");
	}
}


if(process.argv[2]){
  pretty_print(processDirectory(process.argv[2]));
} else {
  runTest();
}
