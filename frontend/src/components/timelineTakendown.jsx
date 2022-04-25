import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent from "@mui/lab/TimelineContent";
import TimelineDot from "@mui/lab/TimelineDot";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
import { Avatar, Typography } from "@mui/material";
import TakendownIcon from "../images/takendownIcon.png";

export default function TimelineTakendown({ heartrate, enemy, time }) {
	return (
		<TimelineItem>
			<TimelineOppositeContent
				sx={{ m: "auto 0" }}
				align="right"
				variant="body2"
				color="text.secondary"
			>
				<Typography>{heartrate} bpm</Typography>
				<Typography>{time}</Typography>
			</TimelineOppositeContent>
			<TimelineSeparator>
				<TimelineConnector />
				<TimelineDot>
					<Avatar alt="Takendown" src={TakendownIcon} />
				</TimelineDot>
				<TimelineConnector />
			</TimelineSeparator>
			<TimelineContent sx={{ py: "30px", px: 4 }}>
				<Typography variant="h6" component="span">
					Takendown
				</Typography>
				<Typography>By: {enemy}</Typography>
			</TimelineContent>
		</TimelineItem>
	);
}
