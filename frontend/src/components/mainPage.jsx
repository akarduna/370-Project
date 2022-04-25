import { Fragment, useState } from "react";
import { Button, TextField, Typography } from "@mui/material";
import Timeline from "@mui/lab/Timeline";
import TimelineDragon from "./timelineDragon";
import TimelineTakedown from "./timelineTakedown";
import TimelineTakendown from "./timelineTakendown";
import TimelineStart from "./timelineStart";
import TimelineEnd from "./timelineEnd";
import { Box } from "@mui/system";
import TimelineBaron from "./timelineBaron";

export default function MainPage() {
	const [val, setVal] = useState("");
	const [val2, setVal2] = useState("");
	const [helpMsg, setHelpMsg] = useState(false);
	const [timelineVisible, setTimelineVisible] = useState(false);

	const handleTypeChange = (event) => {
		setVal(event.target.value);
	};

	const handleSubmit = () => {
		if (!val) {
			setHelpMsg(true);
		} else {
			setVal2(val);
			console.log("Submitted: " + val);
			setVal("");
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
					<Box>
						<TextField
							value={val}
							onChange={handleTypeChange}
							placeholder="Enter match ID"
							error={val ? false : true}
						/>
						<Button onClick={handleSubmit}>Submit</Button>
					</Box>
				)}
			</Box>
			{timelineVisible ? (
				<>
					<Typography variant="h5">
						Displaying information for match: {val2}
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
