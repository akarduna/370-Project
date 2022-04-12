import { Fragment, useState } from "react";
import { Button, TextField, Typography } from "@mui/material";

export default function MainPage() {
	const [val, setVal] = useState("Default");

	const handleTypeChange = (event) => {
		setVal(event.target.value);
	};

	const handleSubmit = () => {
		console.log("Submitted: " + val);
	};

	return (
		<Fragment>
			<Typography variant="h3">League of Legends Heartbeat Data</Typography>
			<TextField
				value={val}
				onChange={handleTypeChange}
				placeholder="Enter match ID"
			/>
			<Button onClick={handleSubmit}>Submit</Button>
		</Fragment>
	);
}
