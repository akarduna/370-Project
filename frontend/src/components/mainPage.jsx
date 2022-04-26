import { Button, Stack, TextField, Typography } from "@mui/material";
import { Fragment, useState } from "react";

import $ from "jquery";
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
	const [time, setTime] = useState();
	const [loading, setLoading] = useState(false);
	const handleTypeChange = (event) => {
		setVal(event.target.value);
	};

	const handleTypeChange2 = (event) => {
		setGamesBack(event.target.value);
	};
	
	function createTimeLine(data){
		const focus = data["player"][2];
		const events = data["events"];
		const timeLine = events.map(function(event) {
			if(event[0] == "obj" && event[1] == "dragon"){
				return <TimelineDragon heartrate={-1} type={event[2]} time={event[4]}/>
			}
			if(event[0] == "obj" && event[1] == "baron"){
				return <TimelineBaron heartrate={-1} time={event[3]}/>
			}
			if(event[0] == "kill" && event[1] == focus){
				return <TimelineTakedown heartrate={-1} enemy={2} time={event[4]}/>
			}
		});
		console.log(timeLine)
		return timeLine;
	}

	const handleSubmit = () => {
		if (!val) {
			setHelpMsg(true);
		} else {
			setLoading(true);
			setVal2(val);
			setGamesBack2(gamesBack)
			console.log("Submitted: " + val + " and " + gamesBack);
			const url = 'http://127.0.01:5000/RIOT_DATA';
			$.ajax(
				url,
				{
					type: `POST`,
					contentType: "application/json",
					data : JSON.stringify({
						"summoner_name": val,
						"game_number": gamesBack
					  }),
					success: function (data, status, xhr) {
						$('p').append('status: ' + status + ', data: ' + data);
						const timeLine = createTimeLine(data);
						setTime(timeLine);
					},
					error: function (jqXhr, textStatus, errorMessage) {
							$('p').append('Error' + errorMessage);
				}
				});
			setVal("");
			setGamesBack("")
			setTimelineVisible(true);
			setHelpMsg(false);
			setLoading(false);
		}
	};

	const handleReset = () => {
		console.log("Reset");
		setTime(<l1></l1>)
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
			{timelineVisible && !loading ? (
				<>
					<Typography variant="h5">
						Displaying information for summoner: <strong>{val2}</strong> from <strong>{gamesBack2}</strong> games back	
					</Typography>
					<Timeline position="left">
						<TimelineStart />
						{time}
						<TimelineEnd />
					</Timeline>
				</>
			) : null}
			{loading ? <Typography>Loading...</Typography> : null}
		</Fragment>
	);
}
