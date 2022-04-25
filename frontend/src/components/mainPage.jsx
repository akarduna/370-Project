import { Fragment, useState } from "react";
import { Button, TextField, Typography } from "@mui/material";
import Timeline from "@mui/lab/Timeline";
import TimelineDragon from "./timelineDragon";
import TimelineTakedown from "./timelineTakedown";
import TimelineTakendown from "./timelineTakendown";
import TimelineStart from "./timelineStart";
import TimelineEnd from "./timelineEnd";

export default function MainPage() {
	const [val, setVal] = useState("");

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
			<Timeline position="left">
				<TimelineStart />
				<TimelineDragon heartrate={20} type={"Ocean"} time={"10 secs"} />
				<TimelineTakedown heartrate={56} enemy={"Jhin"} time={"10 secs"} />
				<TimelineTakendown heartrate={56} enemy={"Pyke"} time={"12 secs"} />
				<TimelineEnd />
			</Timeline>
		</Fragment>
	);
}
