import { Button, Stack, TextField, Typography } from "@mui/material";
import { Fragment, useState } from "react";

import { Box } from "@mui/system";
import Timeline from "@mui/lab/Timeline";
import TimelineBaron from "./timelineBaron";
import TimelineDragon from "./timelineDragon";
import TimelineEnd from "./timelineEnd";
import TimelineStart from "./timelineStart";
import TimelineTakedown from "./timelineTakedown";
import TimelineTakendown from "./timelineTakendown";

export default function MainPage() {
	const [val, setVal] = useState("");
	const [val2, setVal2] = useState("");
	const [gamesBack, setGamesBack] = useState("");
	const [gamesBack2, setGamesBack2] = useState("");
	const [helpMsg, setHelpMsg] = useState(false);
	const [timelineVisible, setTimelineVisible] = useState(false);

	const handleTypeChange = (event) => {
		setVal(event.target.value);
	};

	const handleTypeChange2 = (event) => {
		setGamesBack(event.target.value);
	};

	const handleSubmit = () => {
		if (!val) {
			setHelpMsg(true);
		} else {
			setVal2(val);
			setGamesBack2(gamesBack)
			console.log("Submitted: " + val + " and " + gamesBack);
			setVal("");
			setGamesBack("")
			setTimelineVisible(true);
			setHelpMsg(false);
		}
	};

	const handleReset = () => {
		console.log("Reset");
		setTimelineVisible(false);
	};

	return (
		<Fragment>
			<Typography variant="h3">League of Legends Heartbeat Data</Typography>
			<Box
				style={{
					display: "flex",
					justifyContent: "center",
					padding: "30px 0px 40px 0px",
				}}
			>
				{timelineVisible ? (
					<Button variant="contained" onClick={handleReset}>
						Reset
					</Button>
				) : (
					<Stack >
						<TextField
							value={val}
							onChange={handleTypeChange}
							placeholder="Enter Summoner Name"
							error={val ? false : true}
							style={{padding: "10px"}}
						/>
						<TextField
							value={gamesBack}
							onChange={handleTypeChange2}
							placeholder="Enter number of games back"
							error={gamesBack ? false : true}
						/>
						<Button onClick={handleSubmit}>Submit</Button>
					</Stack>
				)}
			</Box>
			{timelineVisible ? (
				<>
					<Typography variant="h5">
						Displaying information for summoner: <strong>{val2}</strong> at <strong>{gamesBack2}</strong> games back	
					</Typography>
					<Timeline position="left">
						<TimelineStart />
						<TimelineDragon heartrate={20} type={"Ocean"} time={"10 secs"} />
						<TimelineTakedown heartrate={56} enemy={"Jhin"} time={"10 secs"} />
						<TimelineTakendown heartrate={56} enemy={"Pyke"} time={"12 secs"} />
						<TimelineBaron heartrate={95} time={"25 secs"} />
						<TimelineEnd />
					</Timeline>
				</>
			) : null}
		</Fragment>
	);
}
